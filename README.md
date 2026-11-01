# CashierQ

CashierQ is a queue system for a school cashier office, where students waiting to pay (especially during enrollment week) get a ticket and can see their place in line, and cashier staff call, serve, or mark no-shows from a dashboard.

## How to run

You need Python, Git and Docker Desktop. Start Docker Desktop first and wait until it says the engine is running. Then, from the project folder:

1. Create a virtual environment and activate it:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install the packages:

   ```
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`, then open `.env` and replace `change-me` with a password of your own in **both** lines (they must match):

   ```
   copy .env.example .env
   ```

4. Start the PostgreSQL database and wait until `docker compose ps` says it is healthy:

   ```
   docker compose up -d
   docker compose ps
   ```

5. Create the tables and add the starting services:

   ```
   flask --app app db upgrade
   flask --app app seed
   ```

6. Start the app and open http://127.0.0.1:5000 in your browser:

   ```
   flask --app app run --debug
   ```

Use `docker compose down` to stop the database. Your tickets are kept. Do not use `docker compose down -v`, because it deletes the data.

**Note:** The staff dashboard has no login yet. Anyone who opens `/staff` can use it. Staff login is planned for Week 11 (FR-10 in the requirements).

- [Requirements](docs/requirements.md)