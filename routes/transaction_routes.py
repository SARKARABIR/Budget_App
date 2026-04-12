from flask import Blueprint, render_template, request, redirect, jsonify
from services.transaction_service import (
    get_all_transactions,
    get_transaction_by_id,
    get_summary,
    get_budget,
    get_all_categories,
    get_subcategories_by_category,
    add_transaction,
    update_transaction,
    delete_transaction,
    set_budget,
)

transaction_bp = Blueprint("transaction", __name__)


# ──────────────────────────────────────────────
# HOME
# ──────────────────────────────────────────────

@transaction_bp.route("/")
def home():
    month = request.args.get("month")

    transactions = get_all_transactions(month)
    summary      = get_summary(transactions)
    budget       = get_budget()

    return render_template(
        "index.html",
        transactions   = transactions,
        total_income   = summary["total_income"],
        total_expense  = summary["total_expense"],
        balance        = summary["balance"],
        category_data  = summary["category_data"],
        budget         = budget,
        selected_month = month,
    )


# ──────────────────────────────────────────────
# ADD
# ──────────────────────────────────────────────

@transaction_bp.route("/add", methods=["GET", "POST"])
def add_transaction_route():
    categories = get_all_categories()

    if request.method == "POST":
        amount         = float(request.form["amount"])
        tx_type        = request.form["type"]               # "Income" or "Expense"
        date           = request.form["date"]
        category_id    = request.form.get("category") or None
        subcategory_id = request.form.get("subcategory") or None
        details        = request.form.get("details", "")

        add_transaction(amount, tx_type, date, category_id, subcategory_id, details)
        return redirect("/")

    return render_template("add_transaction.html", categories=categories)


# ──────────────────────────────────────────────
# EDIT
# ──────────────────────────────────────────────

@transaction_bp.route("/edit/<int:id>", methods=["GET", "POST"])   # Fixed: was [int:id](int:id)
def edit_transaction_route(id):
    categories = get_all_categories()

    if request.method == "POST":
        amount         = float(request.form["amount"])
        tx_type        = request.form["type"]
        date           = request.form["date"]
        category_id    = request.form.get("category") or None
        subcategory_id = request.form.get("subcategory") or None
        details        = request.form.get("details", "")

        update_transaction(id, amount, tx_type, date, category_id, subcategory_id, details)
        return redirect("/")

    transaction = get_transaction_by_id(id)
    subcategories = []
    if transaction and transaction["category_id"]:
        subcategories = get_subcategories_by_category(transaction["category_id"])

    return render_template(
        "edit_transaction.html",
        transaction   = transaction,
        categories    = categories,
        subcategories = subcategories,
    )


# ──────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────

@transaction_bp.route("/delete/<int:id>")
def delete_transaction_route(id):
    delete_transaction(id)
    return redirect("/")


# ──────────────────────────────────────────────
# BUDGET
# ──────────────────────────────────────────────

@transaction_bp.route("/set_budget", methods=["GET", "POST"])
def set_budget_route():
    if request.method == "POST":
        limit = float(request.form["limit"])
        set_budget(limit)
        return redirect("/")

    return render_template("set_budget.html")


# ──────────────────────────────────────────────
# API — Subcategories (used by JS dropdown)
# ──────────────────────────────────────────────

@transaction_bp.route("/get_subcategories/<int:category_id>")   # Fixed: was missing <>
def get_subcategories_route(category_id):
    rows = get_subcategories_by_category(category_id)
    return jsonify(subcategories=[{"id": r["id"], "name": r["name"]} for r in rows])