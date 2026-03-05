from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    type TEXT,
    category TEXT,
    date TEXT,
    description TEXT
    )
    """)
    
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")

    transactions = cursor.fetchall()

    conn.close()

    return render_template("index.html", transactions=transactions)


@app.route("/add", methods=["GET","POST"])
def add_transaction():
    if request.method == "POST":
        amount = request.form["amount"]
        type = request.form["type"]
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = """
        INSERT INTO transactions (amount, type, category, date, description)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (amount, type, category, date, description))

        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add_transaction.html")

if __name__ == "__main__":
    app.run(debug=True)
    