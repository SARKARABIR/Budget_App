import sqlite3

def get_connection():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subcategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        date TEXT,
        category_id INTEGER,
        subcategory_id INTEGER,
        details TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(id)
        FOREIGN KEY(subcategory_id) REFERENCES subcategories(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_limit REAL
    )
    """)

    conn.commit()
    conn.close()

def seed_categories():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    categories = ["Food","Travel","Family","Rent","Utlilites","Entertainment"]

    for c in categories:
        cursor.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)",(c,))

    conn.commit()
    conn.close()

def seed_subcategories():
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    mapping = {
        "Food": ["Breakfast","Lunch","Dinner","Snacks","Munching"],
        "Travel": ["Flight","Train","Rickshaw","Bus","Metro","Bike"], 
        "Rent": ["PG","Netflix","YouTube"], 
        "Utilities": ["Electricity","Water","Internet","Mobile"], 
        "Entertainment": ["Shows","Sports","Cinema","Events"]
    }

    for category, subs in mapping.items():
        cursor.execute("SELECT id FROM categories WHERE name = ?",(category,))
        result = cursor.fetchone()
        if result is None:
            continue

        category_id = result[0]

        for s in subs:
            cursor.execute(
                "INSERT OR IGNORE INTO subcategories(category_id,name) VALUES(?,?)",
                (category_id,s)
            )
    conn.commit()
    conn.close()

