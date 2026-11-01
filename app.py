"""CashierQ: a queue system for the school cashier office."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

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

def people_ahead(t):
    """Count tickets still waiting that joined before t (one shared line)."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service,
                           ahead=people_ahead(t))

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}

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
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    tickets = db.session.scalars(stmt).all()

    # Shape each ticket the way staff.html expects (id, name, status, service_id)
    queue = [{"id": t.id,
              "name": t.user.name,
              "status": t.status,
              "service_id": t.service_id} for t in tickets]

    all_services = db.session.scalars(db.select(Service).order_by(Service.id)).all()
    names = {s.id: s.name for s in all_services}
    counts = dict(db.session.execute(
        db.select(Ticket.service_id, func.count())
          .where(Ticket.status == "waiting")
          .group_by(Ticket.service_id)).all())
    waiting_counts = {s.id: counts.get(s.id, 0) for s in all_services}

    return render_template("staff.html", queue=queue, services=all_services, names=names,
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