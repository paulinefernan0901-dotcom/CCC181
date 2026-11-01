# Validation

I checked my rules in two places: Flask and PostgreSQL. For Flask, I sent requests with curl so the form was skipped. For the database, I typed statements in psql so Flask was skipped. Either way, bad data should not get in.

## Flask

| Rule | How I tested it | What happened |
| --- | --- | --- |
| Name is required | `curl` POST to `/join` with an empty `name` | Got 400, nothing saved (ticket count stayed at 3) |
| Student ID must match the format | `curl` with `student_id=abcd` | Got 400, nothing saved |
| Email must be valid | `curl` with `email=not-an-email` | Got 400, nothing saved |
| Service must exist | `curl` with `service_id=999` | Got 400, nothing saved |

## Database

| Rule | Constraint type | What I ran | Error PostgreSQL gave |
| --- | --- | --- | --- |
| Ticket needs a real service | FOREIGN KEY | `INSERT INTO tickets (user_id, service_id) VALUES (2, 999);` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Status must be one of the allowed values | CHECK | `UPDATE tickets SET status = 'lost' WHERE id = 2;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Student ID can only be used once | UNIQUE | Inserted a user with `2024-0099`, which already exists | `ERROR: duplicate key value violates unique constraint "users_student_id_key"` |
| Email must contain @ | CHECK | Inserted a user with the email `noatsign` | `ERROR: new row for relation "users" violates check constraint "ck_users_email"` |
| Student ID must match the format | CHECK | Inserted a user with the student ID `abcd` | `ERROR: new row for relation "users" violates check constraint "ck_users_student_id"` |
| Name is required | NOT NULL | Inserted a user with a NULL `name` | `ERROR: null value in column "name" of relation "users" violates not-null constraint` |
| A called ticket needs `called_at` | CHECK | `UPDATE tickets SET status = 'called' WHERE id = 2;` on a waiting ticket | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_called_at"` |
| One active ticket per student per service | Partial UNIQUE index | Inserted a second waiting ticket for user 4 and service 1 | `ERROR: duplicate key value violates unique constraint "uq_tickets_active_user_service"` |
| A service with tickets can't be deleted | RESTRICT | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |

## Defaults

I inserted a good ticket with only the user and the service:

`INSERT INTO tickets (user_id, service_id) VALUES (2, 2) RETURNING id, status, created_at;`

The database filled in `status` as `waiting` and set `created_at` by itself. I deleted that test ticket afterwards.

## No SQL in f-strings

I searched my Python files for SQL written inside f-strings with `git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"`. It printed nothing, so all my queries go through SQLAlchemy.