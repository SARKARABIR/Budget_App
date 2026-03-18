from flask import Blueprint, render_template, request, redirect
from database.db import get_connection

transaction_bp = Blueprint("transaction", __name__)

@transaction_bp.route("/")
def home():


    month = request.args.get("month")

    conn = get_connection()
    cursor = conn.cursor()

    if month:
        cursor.execute("""
        SELECT t.id, t.amount, t.date,
        c.name as category,
        s.name as subcategory,
        t.details
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN subcategories s ON t.subcategory_id = s.id
        WHERE strftime('%Y-%m', t.date) = ?
        """,(month,))
    else:
        cursor.execute("SELECT * FROM transactions")

    transactions = cursor.fetchall()

    total_income = 0
    total_expense = 0

    category_data = {}

    for t in transactions:

        amount = t[1]
        type = t[2]
        category = t[3]

        if type == "Income":
            total_income += amount
        else:
            total_expense += amount

            if category in category_data:
                category_data[category] += amount
            else:
                category_data[category] = amount

    balance = total_income - total_expense

    cursor.execute("SELECT monthly_limit FROM budget")
    budget = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        category_data=category_data,
        budget=budget,
        selected_month=month
    )


@transaction_bp.route("/add", methods=["GET","POST"])
def add_transaction():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        # type = request.form["type"]
        # category = request.form["category"]
        date = request.form["date"]
        # description = request.form["description"]
        category_id = request.form["category"]
        subcategory_id = request.form.get("subcategory")
        details = request.form.get("details")

        if subcategory_id == "":
            subcategory_id = None

        cursor.execute("""
        INSERT INTO transactions (amount,date,category_id,subcategory_id,details)
        VALUES (?,?,?,?,?)
        """,(amount,date,category_id,subcategory_id,details))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_transaction.html")


@transaction_bp.route("/delete/<int:id>")
def delete_transaction(id):


    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


@transaction_bp.route("/edit/[int:id](int:id)", methods=["GET","POST"])
def edit_transaction(id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        amount = request.form["amount"]
        type = request.form["type"]
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        cursor.execute("""
        UPDATE transactions
        SET amount=?, type=?, category=?, date=?, description=?
        WHERE id=?
        """,(amount,type,category,date,description,id))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM transactions WHERE id=?", (id,))
    transaction = cursor.fetchone()

    conn.close()

    return render_template("edit_transaction.html", transaction=transaction)


@transaction_bp.route("/set_budget", methods=["GET","POST"])
def set_budget():


    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        limit = request.form["limit"]

        cursor.execute("DELETE FROM budget")
        cursor.execute("INSERT INTO budget (monthly_limit) VALUES (?)",(limit,))

        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()

    return render_template("set_budget.html")

@transaction_bp.route("/get_subcategories/int:category_id")
def get_subcategories(category_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name FROM subcategories WHERE category_id=?",
        (category_id,)
    )

    subcategories = cursor.fetchall()
    conn.close()

    return {"subcategories": subcategories}

