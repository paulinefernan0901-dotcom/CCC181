"""CashierQ: a queue system for the school cashier office."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me" 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)


@app.get("/")
def index():
    return render_template("index.html")


def active_services():
    stmt = db.select(Service).filter_by(is_active=True).order_by(Service.id)
    return db.session.scalars(stmt).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(), form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    student_id = form.get("student_id", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 100:
        errors["name"] = "Enter your name."
    if len(student_id) < 4 or len(student_id) > 20:
        errors["student_id"] = "Enter your student ID."
    if "@" not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None or not service.is_active:
        errors["service_id"] = "Choose what you need at the cashier."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=active_services(), form=form, errors=errors), 400

    user = db.session.scalar(db.select(User).filter_by(student_id=student_id))
    if user is None:
        user = User(name=name, student_id=student_id, email=email)
    else:
        user.name = name
        user.email = email
    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("You already have an active ticket for that service.", "danger")
        return render_template("join.html", services=active_services(), form=form, errors={}), 409

    flash("You joined the queue.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


# PARTS 8 AND 9 replace every route below. They still use the deleted
# SERVICES and TICKETS lists, so they will show an error until then.
# That is expected at this point in the activity.

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

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = ["Registrar document fees", "Tuition and other fees", "Other payments"]
    for name in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name))
    db.session.commit()
    print("Services are ready.")