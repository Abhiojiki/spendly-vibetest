import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

def create_user(name, email, password):
    conn = get_db()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute('''
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    ''', (name, email, password_hash))
    conn.commit()
    user_id = cursor.lastrowid

    # Prepopulate with static dummy expense data for new users
    sample_expenses = [
        (user_id, 24.50, 'Food', '2026-07-20', 'Artisan coffee & brunch'),
        (user_id, 55.00, 'Transport', '2026-07-21', 'Monthly transit pass'),
        (user_id, 120.00, 'Bills', '2026-07-22', 'Fiber broadband internet'),
        (user_id, 85.00, 'Shopping', '2026-07-22', 'Books and stationery')
    ]
    cursor.executemany('''
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_expenses)
    conn.commit()
    conn.close()
    return user_id

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, created_at FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_expense_stats(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0.0) as total_spent, COUNT(*) as expense_count
        FROM expenses WHERE user_id = ?
    ''', (user_id,))
    stats = cursor.fetchone()

    if stats["expense_count"] == 0:
        # Prepopulate with static dummy expense data if none exist
        sample_expenses = [
            (user_id, 24.50, 'Food', '2026-07-20', 'Artisan coffee & brunch'),
            (user_id, 55.00, 'Transport', '2026-07-21', 'Monthly transit pass'),
            (user_id, 120.00, 'Bills', '2026-07-22', 'Fiber broadband internet'),
            (user_id, 85.00, 'Shopping', '2026-07-22', 'Books and stationery'),
            (user_id, 40.00, 'Entertainment', '2026-07-23', 'Movie tickets')
        ]
        cursor.executemany('''
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_expenses)
        conn.commit()

        cursor.execute('''
            SELECT COALESCE(SUM(amount), 0.0) as total_spent, COUNT(*) as expense_count
            FROM expenses WHERE user_id = ?
        ''', (user_id,))
        stats = cursor.fetchone()

    cursor.execute('''
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM expenses WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
    ''', (user_id,))
    categories = cursor.fetchall()

    cursor.execute('''
        SELECT id, amount, category, date, description
        FROM expenses WHERE user_id = ?
        ORDER BY date DESC, id DESC
        LIMIT 10
    ''', (user_id,))
    recent_expenses = cursor.fetchall()

    conn.close()

    return {
        "total_spent": stats["total_spent"],
        "expense_count": stats["expense_count"],
        "categories": categories,
        "recent_expenses": recent_expenses
    }

def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash('demo123')
    cursor.execute('''
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    ''', ('Demo User', 'demo@spendly.com', password_hash))

    user_id = cursor.lastrowid

    # 8 sample expenses covering all 7 categories
    # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
    sample_expenses = [
        (user_id, 15.50, 'Food', '2026-07-01', 'Morning coffee and pastry'),
        (user_id, 45.00, 'Transport', '2026-07-03', 'Monthly subway pass'),
        (user_id, 120.00, 'Bills', '2026-07-05', 'Electricity bill'),
        (user_id, 30.00, 'Health', '2026-07-08', 'Pharmacy vitamins'),
        (user_id, 65.00, 'Entertainment', '2026-07-10', 'Concert tickets'),
        (user_id, 85.20, 'Shopping', '2026-07-12', 'New headphones'),
        (user_id, 25.00, 'Other', '2026-07-15', 'Charity donation'),
        (user_id, 42.50, 'Food', '2026-07-18', 'Dinner with friends')
    ]

    cursor.executemany('''
        INSERT INTO expenses (user_id, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_expenses)

    conn.commit()
    conn.close()
