"""
transaction_service.py
-----------------------
All database query logic lives here.
Routes should call these functions — never write raw SQL in routes.
Swap SQLite for Snowflake later by only changing this file + db.py.
"""

from database.db import get_connection


# ──────────────────────────────────────────────
# READ
# ──────────────────────────────────────────────

def get_all_transactions(month=None):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        if month:
            cursor.execute("""
                SELECT t.id, t.amount, t.type, t.date,
                       c.name AS category, s.name AS subcategory, t.details
                FROM transactions t
                LEFT JOIN categories    c ON t.category_id    = c.id
                LEFT JOIN subcategories s ON t.subcategory_id = s.id
                WHERE strftime('%Y-%m', t.date) = ?
                ORDER BY t.date DESC
            """, (month,))
        else:
            cursor.execute("""
                SELECT t.id, t.amount, t.type, t.date,
                       c.name AS category, s.name AS subcategory, t.details
                FROM transactions t
                LEFT JOIN categories    c ON t.category_id    = c.id
                LEFT JOIN subcategories s ON t.subcategory_id = s.id
                ORDER BY t.date DESC
            """)
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_all_transactions: {e}")
        return []
    finally:
        conn.close()


def get_transaction_by_id(transaction_id):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.amount, t.type, t.date,
                   t.category_id, t.subcategory_id, t.details,
                   c.name AS category, s.name AS subcategory
            FROM transactions t
            LEFT JOIN categories    c ON t.category_id    = c.id
            LEFT JOIN subcategories s ON t.subcategory_id = s.id
            WHERE t.id = ?
        """, (transaction_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"[ERROR] get_transaction_by_id: {e}")
        return None
    finally:
        conn.close()


def get_summary(transactions):
    total_income  = 0.0
    total_expense = 0.0
    category_data = {}
    for t in transactions:
        amount   = t["amount"]
        tx_type  = t["type"]
        category = t["category"] or "Uncategorized"
        if tx_type == "Income":
            total_income += amount
        else:
            total_expense += amount
            category_data[category] = category_data.get(category, 0) + amount
    return {
        "total_income":  total_income,
        "total_expense": total_expense,
        "balance":       total_income - total_expense,
        "category_data": category_data,
    }


def get_budget():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monthly_limit FROM budget LIMIT 1")
        row = cursor.fetchone()
        return row["monthly_limit"] if row else None
    except Exception as e:
        print(f"[ERROR] get_budget: {e}")
        return None
    finally:
        conn.close()


def get_all_categories():
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY name")
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_all_categories: {e}")
        return []
    finally:
        conn.close()


def get_subcategories_by_category(category_id):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name FROM subcategories WHERE category_id = ? ORDER BY name",
            (category_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] get_subcategories_by_category: {e}")
        return []
    finally:
        conn.close()


# ──────────────────────────────────────────────
# WRITE
# ──────────────────────────────────────────────

def add_transaction(amount, tx_type, date, category_id, subcategory_id, details):
    try:
        if not amount or float(amount) <= 0:
            raise ValueError("Amount must be a positive number.")
        if not date:
            raise ValueError("Date is required.")
        if not tx_type:
            raise ValueError("Type (Income/Expense) is required.")
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (amount, type, date, category_id, subcategory_id, details)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (float(amount), tx_type, date, category_id or None, subcategory_id or None, details))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"[ERROR] add_transaction: {e}")
        raise
    finally:
        conn.close()


def update_transaction(transaction_id, amount, tx_type, date, category_id, subcategory_id, details):
    try:
        if not amount or float(amount) <= 0:
            raise ValueError("Amount must be a positive number.")
        if not date:
            raise ValueError("Date is required.")
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions
            SET amount=?, type=?, date=?, category_id=?, subcategory_id=?, details=?
            WHERE id=?
        """, (float(amount), tx_type, date, category_id or None, subcategory_id or None, details, transaction_id))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] update_transaction: {e}")
        raise
    finally:
        conn.close()


def delete_transaction(transaction_id):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] delete_transaction: {e}")
        raise
    finally:
        conn.close()


def set_budget(monthly_limit):
    try:
        if not monthly_limit or float(monthly_limit) <= 0:
            raise ValueError("Budget limit must be a positive number.")
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM budget")
        cursor.execute("INSERT INTO budget (monthly_limit) VALUES (?)", (float(monthly_limit),))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] set_budget: {e}")
        raise
    finally:
        conn.close()