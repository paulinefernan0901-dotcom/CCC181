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
    # Count only people still waiting ahead of this ticket for the same service
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))


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
    return "Staff dashboard coming soon"