"""CashierQ: a queue system for the school cashier office."""
from flask import Flask, abort, flash, redirect, render_template, request, url_for  # noqa: F401 (used in later parts)

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable


SERVICES = [
    {"id": 1, "name": "Registrar document fees"},
    {"id": 2, "name": "Tuition and other fees"},
    {"id": 3, "name": "Other payments"}
]

# Each ticket: number, name, student_id, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Luna", "student_id": "2024-0001", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Lina", "student_id": "2024-0002", "service_id": 2, "status": "waiting"},
    {"number": 3, "name": "Nona", "student_id": "2024-0003", "service_id": 1, "status": "waiting"},
]


@app.get("/")
def index():
    return render_template("index.html")


@app.route("/join")
def join_form():
    return render_template("join.html")


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"