# from flask import Flask, render_template, request, redirect
# import sqlite3

# app = Flask(__name__)
# def init_db():
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
# # ---------------------------------  DATABASE CREATION  ---------------------------------#
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS transactions(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     amount REAL,
#     type TEXT,
#     category TEXT,
#     date TEXT,
#     description TEXT
#     )
#     """)
# # ---------------------------------  DATABASE CREATION  ---------------------------------#   
#     conn.commit()
#     conn.close()

# init_db()

# @app.route("/")
# def home():
    
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
# # ---------------------------------  INCOME, EXPENSE, BALANCE LOGIC  ---------------------------------# 
#     cursor.execute("SELECT * FROM transactions")
#     transactions = cursor.fetchall()

#     total_income = 0
#     total_expense = 0

#     for t in transactions:
#         amount = t[1]
#         type = t[2]

#         if type == "income":
#             total_income += amount
#         else:
#             total_expense += amount
        
#     balance = total_income + total_expense
    
#     category_data = {}

#     for t in transactions:

#         amount = t[1]
#         type = t[2]
#         category = t[3]

#         if type == "Expense":

#             if category in category_data:
#                 category_data[category] += amount
#             else:
#                 category_data[category] = amount



#     conn.close()

#     return render_template(
#         "index.html", 
#         transactions=transactions,
#         total_income = total_income,
#         total_expense = total_expense,
#         balance = balance,
#         category_data=category_data
#         )
# # ---------------------------------  INCOME, EXPENSE, BALANCE LOGIC  ---------------------------------# 


# # --------------------------------- INPUT DATA IN TABLE  ---------------------------------# 

# @app.route("/add", methods=["GET","POST"])
# def add_transaction():
#     if request.method == "POST":
#         amount = request.form["amount"]
#         type = request.form["type"]
#         category = request.form["category"]
#         date = request.form["date"]
#         description = request.form["description"]

#         conn = sqlite3.connect("database.db")
#         cursor = conn.cursor()

#         query = """
#         INSERT INTO transactions (amount, type, category, date, description)
#         VALUES (?, ?, ?, ?, ?)
#         """
#         cursor.execute(query, (amount, type, category, date, description))

#         conn.commit()
#         conn.close()

#         return redirect("/")
#     return render_template("add_transaction.html")

# # --------------------------------- INPUT DATA IN TABLE  ---------------------------------# 
# # --------------------------------- DELETE DATA IN TABLE  ---------------------------------# 

# @app.route("/delete/<int:id>")
# def delete_transaction(id):

#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))

#     conn.commit()
#     conn.close()

#     return redirect("/")
# # --------------------------------- DELETE DATA IN TABLE  ---------------------------------# 
# # --------------------------------- EDIT DATA IN TABLE  ---------------------------------# 

# @app.route("/edit/<int:id>", methods=["GET","POST"])
# def edit_transaction(id):

#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     if request.method == "POST":

#         amount = request.form["amount"]
#         type = request.form["type"]
#         category = request.form["category"]
#         date = request.form["date"]
#         description = request.form["description"]

#         cursor.execute("""
#         UPDATE transactions
#         SET amount=?, type=?, category=?, date=?,description=?
#         WHERE id=?
#         """,(amount,type,category,date,description,id))

#         conn.commit()
#         conn.close()

#         return redirect("/")
    
#     cursor.execute("SELECT * FROM transactions WHERE id=?",(id,))
#     transaction = cursor.fetchone()

#     conn.close()

#     return render_template("edit_transaction.html",transaction = transaction)




# if __name__ == "__main__":
#     app.run(debug=True)
    


######################################################################


from flask import Flask
from routes.transaction_routes import transaction_bp
from database.db import init_db, seed_categories, seed_subcategories
app = Flask(__name__)

init_db()
seed_categories()
seed_subcategories()

app.register_blueprint(transaction_bp)

if __name__ == "__main__":
    app.run(debug=True)
