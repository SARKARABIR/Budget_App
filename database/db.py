import sqlite3

def get_connection():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():


    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        date TEXT,
        category TEXT,
        subcategory TEXT,
        details TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_limit REAL
    )
    """)

    conn.commit()
    conn.close()

