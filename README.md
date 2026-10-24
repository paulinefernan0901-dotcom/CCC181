# CashierQ

CashierQ is a queue system for a school cashier office, where students waiting to pay (especially during enrollment week) get a ticket and can see their place in line, and cashier staff call, serve, or mark no-shows from a dashboard.

## How to run

To run it, create a virtual environment (`python -m venv .venv`), activate it (`.venv\Scripts\activate`), install the packages (`pip install -r requirements.txt`), and then start the app with `flask --app app run --debug`.



**Note:** The staff dashboard has no login yet. Anyone who opens `/staff` can use it. Staff login comes in a later week.