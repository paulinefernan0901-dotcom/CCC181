# Schema review

### 1. **Coverage:** does every requirement in `docs/requirements.md` marked *Stores data? = Yes* have a table or column for it? Does each persona's top task from Week 3 have the data it needs? Is there any table or column that **no** requirement needs? (Then either a requirement is missing, or the column is.)
- **Works well:** Every requirement that stores data (FR-01, 02, 04, 05, 06, 07, 08, 11, 12) has a table or column. Additionally, Dona's and Teresa's top tasks are covered too.
- **Problem:** The `users.email` is collected in FR-01, but at the moment, none of my requirements use it. The alerts that will be utilized by email are out of scope and the cashier calls people by ticket number, so I'm storing personal data the app doesn't need yet.
- **Change:** I decided to keep the `email` column because the join form already collects it.

### 2. **One fact in one place:** is any fact stored in more than one row or table?
- **Works well:** The student's name, student ID and email are each stored once in `users`, and a service's name is stored once in `services`. The tickets only point to them with `user_id` and `service_id`, so no fact is copied.
- **Problem:** None found. A returning student is matched by `student_id` and reuses their existing `users` row, so a new name or email replaces the old one in that one row and is never copied into a second row.
- **Change:** None.

### 3. **Facts, not results:** am I storing anything I could compute instead, such as a position, a count or a waiting time?
- **Works well:** The place in line, the number of people ahead, the counts and the waiting times are never saved. Instead, they are worked out from `created_at`, `called_at` and `status` whenever they are needed, so they are always correct.
- **Problem:** None found.
- **Change:** None.

### 4. **Bad data:** think of the mistakes your personas could make (a double tap, a typo in an email, picking the wrong service). Which constraint stops each one from reaching the database?
- **Works well:** A ticket can't be saved for a student or service that doesn't exist because the foreign keys will block it. A mistyped status is rejected by the CHECK on `status`, and an email with no @ is rejected by the CHECK on `email`.
- **Problem 1:** The join button already locks after one tap, so a double tap doesn't create two tickets in the app. But that protection only exists in the browser. A student could still end up with two waiting tickets for the same service by submitting from two tabs or two devices, and nothing in the database would stop it, because UNIQUE on `student_id` only prevents duplicate students, not duplicate tickets
- **Problem 2:** A ticket could have the status `called` with an empty `called_at`, or the status `waiting` with a `called_at` value, so the two columns could disagree.
- **Change:** I added a unique index on `tickets` (`user_id`, `service_id`) that only applies while a ticket is waiting or called, so the database refuses a second active ticket for the same student and service. I also added a CHECK so `called_at` is filled in exactly when the status is called, served or no-show.

### 5. **Deletes:** for every foreign key, did I choose RESTRICT, CASCADE or SET NULL on purpose? Would any delete destroy history the staff need?
- **Works well:** Both foreign keys use RESTRICT on purpose, so deleting a student or a service can't erase old tickets that the staff need for their reports.
- **Problem:** None found
- **Change:** None

### 6. **Types:** is every moment in time a `timestamptz`? Is anything stored as text that should be a number, a date or a true/false value?
- **Works well:** `created_at` and `called_at` are `timestamptz`, `is_active` is a boolean, and `student_id` is text because it can have leading zeros.
- **Problem:** None found
- **Change:** None