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
    conn.close()
    return user_id

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
