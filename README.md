# QuickPoll

Django + Django REST Framework + HTML/HTMX + PostgreSQL.
Team: **Mayank** (database + business logic), **Ravinder** (REST API), **Rishi** (frontend).

This starter has only the Docker setup and an empty Django project. The app folders
(`accounts/`, `polls/`, `web/`) do not exist yet: Mayank creates them empty with one command
(section 4) and then each of you builds your own part.

---------------------------------------------------------------------

## 1. Install (Mac and Windows, same steps)

1. Install **Docker Desktop** from docker.com
   - Mac: choose Apple chip or Intel.
   - Windows 10/11: keep the **WSL 2** option ticked, restart if asked.
2. Install **Git** and **VS Code**.
3. Open Docker Desktop and wait until it says it is running.

You do NOT need to install Python or PostgreSQL.

## 2. Run

```
git clone <repo-url>
cd quickpoll
docker compose up --build
```
First run takes a few minutes. When you see `Starting development server`, open
http://127.0.0.1:8000 : it should say **QuickPoll is running**.
Stop with `Ctrl+C`.

## 3. Daily Docker commands (second terminal, inside the project folder)

| What | Command |
|---|---|
| Start again | `docker compose up` |
| Stop everything | `docker compose down` |
| Run any Django command | `docker compose exec web python manage.py <command>` |
| Create migrations (Mayank only) | `docker compose exec web python manage.py makemigrations` |
| Apply migrations | `docker compose exec web python manage.py migrate` |
| Run tests | `docker compose exec web python manage.py test` |
| Create admin user | `docker compose exec web python manage.py createsuperuser` |
| PostgreSQL shell | `docker compose exec db psql -U quickpoll quickpoll` |
| Backup database | `docker compose exec db pg_dump -U quickpoll quickpoll > backup.sql` |
| Delete database and start fresh | `docker compose down -v` |
| Logs | `docker compose logs -f web` |

Edit code in VS Code normally; the server reloads by itself.
Run `docker compose up --build` again only after `requirements.txt` or `Dockerfile` changes.

## 4. Order to start (important)

**Step 1 - Mayank, Day 1 (others wait for the push):**
```
docker compose exec web python manage.py startapp accounts
docker compose exec web python manage.py startapp polls
docker compose exec web python manage.py startapp web
```
This creates the three empty app folders. Then:
1. Write the custom `User` (with a `role` field) in `accounts/models.py`.
2. In `config/settings.py`: add `"accounts"`, `"polls"`, `"web"` to `INSTALLED_APPS` and
   uncomment `AUTH_USER_MODEL = "accounts.User"`.
3. Write Poll, Option, Vote in `polls/models.py`.
4. `makemigrations`, then `migrate`, commit everything and push.

**Step 2 - everyone else:** `git pull`, then `docker compose up --build` and
`docker compose exec web python manage.py migrate`.

**Step 3 - work in parallel** on your own files.

## 5. Who owns which files

| Person | Files |
|---|---|
| Mayank | `accounts/models.py`, `polls/models.py`, `polls/migrations/`, `polls/selectors.py`, `polls/services.py`, `polls/admin.py` |
| Ravinder | `polls/serializers.py`, `polls/views.py`, `polls/permissions.py`, `polls/urls.py` |
| Rishi | everything inside `web/` (views, urls, templates, static) |
| Shared (tell the group) | `config/settings.py`, `config/urls.py`, `requirements.txt`, `docker-compose.yml` |

Layer rule: web pages and API never hold business rules; they call
`polls/services.py` (rules) and `polls/selectors.py` (reading data).

## 6. Git routine

```
git checkout main
git pull                              # always first
git checkout -b feature/short-name    # your own branch
# ... work ...
git add .
git commit -m "What you did"
git push -u origin feature/short-name # open Pull Request, teammate reviews, merge
```
Only Mayank creates migrations, so migration files never clash.
After every pull: `docker compose up --build` and `... manage.py migrate`.

## 7. Problems

| Problem | Fix |
|---|---|
| `Cannot connect to the Docker daemon` | Open Docker Desktop, wait until running |
| Port 8000 already in use | Change `"8000:8000"` to `"8001:8000"` in `docker-compose.yml` |
| `relation ... does not exist` | Run `migrate` |
| Windows: `exec ... no such file` | `git config --global core.autocrlf input`, then re-clone |
| `startapp ... conflicts with the name of an existing module` | The folder already exists. Delete the empty folder and run `startapp` again |
# QucikPoll-
