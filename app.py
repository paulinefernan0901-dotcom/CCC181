"""CashierQ: a queue system for the school cashier office."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable


SERVICES = [
    {"id": 1, "name": "Registrar document fees"},
    {"id": 2, "name": "Tuition and other fees"},
    {"id": 3, "name": "Other payments"},
]

# Each ticket: number, name, student_id, email, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Luna", "student_id": "2024-0001", "email": "luna@school.edu",
     "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Lina", "student_id": "2024-0002", "email": "lina@school.edu",
     "service_id": 2, "status": "waiting"},
    {"number": 3, "name": "Nona", "student_id": "2024-0003", "email": "nona@school.edu",
     "service_id": 1, "status": "waiting"},
]


def find_ticket(ticket_id):
    return next((t for t in TICKETS if t["number"] == ticket_id), None)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    student_id = form.get("student_id", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)

    # Never trust form input: the server checks every field, even if the browser already did
    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if len(student_id) < 4:
        errors["student_id"] = "Enter your student ID."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose what you need at the cashier."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = max((t["number"] for t in TICKETS), default=0) + 1
    TICKETS.append({"number": number, "name": name, "student_id": student_id,
                    "email": email, "service_id": service_id, "status": "waiting"})
    flash("You joined the queue.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    # Count everyone still waiting ahead of this ticket, whatever their service
    ahead = [x for x in TICKETS
             if x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    # Same shared-line rule as the ticket route, so the two numbers always agree
    ahead = sum(1 for x in TICKETS
                if x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    if t["status"] in ("waiting", "called"):
        t["status"] = "no-show"
        flash(f"Ticket #{ticket_id} left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}
    waiting_counts = {s["id"]: sum(1 for t in TICKETS
                                   if t["service_id"] == s["id"] and t["status"] == "waiting")
                      for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES, names=names,
                           selected=service_id, waiting_counts=waiting_counts)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    waiting = [t for t in TICKETS
               if t["status"] == "waiting" and (not service_id or t["service_id"] == service_id)]
    if waiting:
        waiting[0]["status"] = "called"
        flash(f"Ticket #{waiting[0]['number']} called.", "info")
    else:
        flash("No one is waiting.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    # Actions that change data use POST, never a plain link
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = find_ticket(ticket_id)
    if t is None or new_status is None:
        abort(404)
    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))