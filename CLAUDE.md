# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Run application:** `python app.py` (starts the Flask development server on port 5001)
- **Run tests:** `pytest`

## Architecture & Structure

- **`app.py`**: Core Flask application containing route handlers (`/`, `/register`, `/login`, `/terms`, `/privacy`, and placeholder routes for steps).
- **`database/`**: Database configuration module (`db.py`) for SQLite connection, initialization, and seeding.
- **`templates/`**: Jinja2 HTML templates extending `base.html` (includes landing page, authentication views, terms, and privacy policy).
- **`static/`**: Static assets including custom CSS (`css/style.css`) and client-side JavaScript (`js/main.js`).
