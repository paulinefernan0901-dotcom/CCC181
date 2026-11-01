# Persistence

## Restart test

I started with 9 tickets across 2 services. One was served, one was called, one student had left the queue, and the rest were still waiting. Before touching anything, I took two screenshots: the staff dashboard, and the result of `SELECT id, status, service_id, created_at FROM tickets ORDER BY id;`.

Then I shut everything down. I stopped Flask with Ctrl+C and ran `docker compose down`, and `docker compose ps` showed nothing running. After that I ran `docker compose up -d`, waited until the database said `healthy`, started Flask again, and took the same two screenshots.

### Before

![Dashboard before](screenshots/before-dashboard.png)

![SQL before](screenshots/before-sql.png)

### After

![Dashboard after](screenshots/after-dashboard.png)

![SQL after](screenshots/after-sql.png)

## Result

Nothing changed. All 9 tickets came back with the same statuses and the same `created_at` times, and the dashboard showed the same waiting counts. The data lives in the `pgdata` volume, so `docker compose down` removes the container but not the tickets. The NFR-01 (no ticket is lost when the server or database restarts) passed.

## Rebuild from scratch

I also wanted to be sure my migrations can build the whole database on a clean machine, so I deleted everything and started over:

docker compose down -v
docker compose up -d
flask --app app db upgrade
flask --app app seed


`down -v` removed the container, the network and the `pgdata` volume, so every ticket was gone. After the new database was `healthy`, `upgrade` ran both migrations in order (`97c40e14454a` for the initial tables, then `d22f5723e1d0` for the student ID format check), and `seed` added my three services. `\dt` listed `users`, `services`, `tickets` and `alembic_version`.

The app opened, all three services showed on the join form, and I could join the queue and see the new ticket on the staff dashboard. So the migrations and the seed command are enough to rebuild my database on any computer.