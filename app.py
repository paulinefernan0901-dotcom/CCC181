"""CashierQ: a queue system for the school cashier office."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

import os
import re
from datetime import timedelta, timezone

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

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving
STUDENT_ID_RE = re.compile(r"^\d{4}-\d{4}$")


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""


def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.id)).all()


def active_services():
    stmt = db.select(Service).filter_by(is_active=True).order_by(Service.id)
    return db.session.scalars(stmt).all()


def people_ahead(t):
    """Count tickets still waiting that joined before t (one shared line)."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)


@app.get("/")
def index():
    return render_template("index.html")


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
    if not STUDENT_ID_RE.match(student_id):
        errors["student_id"] = "Invalid ID format. Use YYYY-NNNN, for example 2023-1234."
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
        active = db.session.scalar(
            db.select(Ticket).where(Ticket.user_id == user.id,
                                    Ticket.service_id == service.id,
                                    Ticket.status.in_(["waiting", "called"])))
        if active:
            db.session.rollback()
            flash("You already have an active ticket for that service.", "danger")
            return render_template("join.html", services=active_services(), form=form, errors={}), 409
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
    t = db.get_or_404(Ticket, ticket_id)
    # Soft delete: the row stays for reports. Only a waiting ticket can leave,
    # because your schema requires called_at on every called ticket.
    if t.status == "waiting":
        t.status = "left"
        db.session.commit()
        flash(f"Ticket #{ticket_id} left the queue.", "info")
    else:
        flash("Only a waiting ticket can leave the queue.", "danger")
    return redirect(url_for("index"))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()

    services = all_services()
    counts = dict(db.session.execute(
        db.select(Ticket.service_id, func.count())
          .where(Ticket.status == "waiting")
          .group_by(Ticket.service_id)).all())
    waiting_counts = {s.id: counts.get(s.id, 0) for s in services}

    return render_template("staff.html", queue=queue, services=services,
                           selected=service_id, waiting_counts=waiting_counts)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .filter_by(status="waiting")
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    t = db.session.scalar(stmt.limit(1))
    if t is None:
        flash("No one is waiting.", "info")
    else:
        t.status = "called"
        t.called_at = func.now()  # the database fills in the time
        db.session.commit()
        flash(f"Ticket #{t.id} called.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


TRANSITIONS = {"call": ("waiting", "called"),
               "serve": ("called", "served"),
               "no-show": ("called", "no-show")}


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    # Actions that change data use POST, never a plain link
    rule = TRANSITIONS.get(action)
    if rule is None:
        abort(404)
    required, new_status = rule
    t = db.get_or_404(Ticket, ticket_id)
    if t.status != required:
        flash(f"Ticket #{ticket_id} is {t.status}, so it can't be marked {new_status}.", "danger")
        return redirect(url_for("staff_dashboard"))
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()  # the database fills in the time
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("The database refused that change.", "danger")
        return redirect(url_for("staff_dashboard"))
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))


@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter a service name (up to 60 characters).", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name))
    try:
        db.session.commit()
        flash(f"Service “{name}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter a service name (up to 60 characters).", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    # A checkbox that is not ticked is not sent at all
    s.is_active = request.form.get("is_active") == "on"
    try:
        db.session.commit()
        flash(f"Service “{name}” saved.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    name = s.name
    if s.tickets:
        flash(f"“{name}” has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Service “{name}” deleted.", "warning")
    return redirect(url_for("services_list"))


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