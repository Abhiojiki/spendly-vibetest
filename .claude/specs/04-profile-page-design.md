# Spec: Profile Page Design

## Overview

This feature implements the Profile Page for Spendly, converting the `/profile` stub into a fully functional view where authenticated users can view their account details (name, email, member since date) and summary statistics of their expenses (total spent, expense count, breakdown by category). It ensures unauthorized users are redirected to the login page, and adds navigation links in the header to make the profile easily accessible.

## Depends on

- Step 01 — Database Setup (`users` and `expenses` tables, database helper functions)
- Step 02 — Registration (`users` table population and structure)
- Step 03 — Login and Logout (session authentication with `session["user_id"]`)

## Routes

- `GET /profile` — render the user profile view with account information and expense statistics — logged-in (requires `session["user_id"]`, redirects to login if unauthenticated)

## Database changes

No new database schema changes. Utilizes existing `users` and `expenses` tables. New database helper functions may be added to `database/db.py` to fetch user details and aggregate expense statistics (e.g., total amount, count, category totals) for a given user ID.

## Templates

- **Create:** `templates/profile.html` — displays user account card, summary stats cards (total expenses, total amount spent), and a categorized breakdown or recent activity list.
- **Modify:** `templates/base.html` — update navigation header to include a link to `/profile` and ensure proper login/logout state links.

## Files to change

- `app.py` — replace the `/profile` stub route with a proper view handler that checks authentication, fetches user details and expense summaries from the database, and renders `templates/profile.html`.
- `database/db.py` — add helper functions for retrieving user profile data and calculating expense statistics by `user_id`.
- `templates/base.html` — update header navigation to link to `/profile` when logged in.

## Files to create

- `templates/profile.html` — profile page template extending `base.html`.

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings in SQL
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode paths
- Protect `/profile` route: check if `session.get("user_id")` exists; if not, flash an error and redirect to `url_for("login")`
- Aggregate expense statistics efficiently using SQL queries in `database/db.py`

## Definition of done

- [ ] Visiting `GET /profile` while not logged in redirects to `/login` with an appropriate flash message
- [ ] Visiting `GET /profile` while logged in successfully renders `templates/profile.html` extending `base.html`
- [ ] The profile page displays the user's name, email address, and member since date correctly from the database
- [ ] The profile page displays accurate expense statistics (total amount spent, total number of expenses) for the logged-in user
- [ ] Navigation header in `templates/base.html` provides a working link to `/profile` when authenticated
- [ ] The `/profile` route no longer returns the raw stub string
