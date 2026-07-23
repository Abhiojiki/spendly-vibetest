from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import sqlite3
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, get_user_expense_stats
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return render_template("register.html")

        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for("login"))
    else:
        abort(405)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("All fields are required.", "error")
            return render_template("login.html")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("profile"))
    else:
        abort(405)


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    if not user:
        session.clear()
        flash("User not found. Please log in again.", "error")
        return redirect(url_for("login"))

    # Static dummy fake data for profile statistics and expenses
    stats = {
        "total_spent": 324.50,
        "expense_count": 5,
        "categories": [
            {"category": "Bills", "total": 120.00, "count": 1},
            {"category": "Shopping", "total": 85.00, "count": 1},
            {"category": "Transport", "total": 55.00, "count": 1},
            {"category": "Entertainment", "total": 40.00, "count": 1},
            {"category": "Food", "total": 24.50, "count": 1}
        ],
        "recent_expenses": [
            {"date": "2026-07-23", "category": "Entertainment", "description": "Movie tickets", "amount": 40.00},
            {"date": "2026-07-22", "category": "Shopping", "description": "Books and stationery", "amount": 85.00},
            {"date": "2026-07-22", "category": "Bills", "description": "Fiber broadband internet", "amount": 120.00},
            {"date": "2026-07-21", "category": "Transport", "description": "Monthly transit pass", "amount": 55.00},
            {"date": "2026-07-20", "category": "Food", "description": "Artisan coffee & brunch", "amount": 24.50}
        ]
    }

    return render_template("profile.html", user=user, stats=stats)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
