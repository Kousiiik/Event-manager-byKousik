from flask import Flask, render_template, request, redirect
from flask.wrappers import Request
import sqlalchemy
from sqlalchemy.sql.expression import null
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "mydatabase.db")
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)


@app.route("/")
def add():
    return render_template("add.html")


@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    total = 0
    t_household = 0
    t_entertainment = 0
    t_education = 0
    t_health = 0
    t_eat = 0
    t_other = 0
    for expense in expenses:
        total += expense.amount
        if expense.category == 'Household':
            t_household += expense.amount

        elif expense.category == 'Entertainment':
            t_entertainment += expense.amount

        elif expense.category == 'Education':
            t_education += expense.amount

        elif expense.category == 'Health':
            t_health += expense.amount

        elif expense.category == 'Eat Outside':
            t_eat += expense.amount

        elif expense.category == 'Other':
            t_other += expense.amount

    print(total, t_household, t_entertainment,
          t_education, t_health, t_eat, t_other)
    return render_template("expenses.html", expenses=expenses, total=total, t_household=t_household, t_entertainment=t_entertainment, t_education=t_education, t_health=t_health, t_eat=t_eat, t_other=t_other)


@app.route("/addexpense", methods=["POST"])
def addexpense():
    date = request.form['date']
    name = request.form['name']
    amount = request.form['amount']
    category = request.form['category']
    expense = Expense(date=date, name=name, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")


@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")


@app.route('/updateexpense/<int:id>')
def updateexpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template("updateexpense.html", expense=expense)


@app.route('/edit', methods=['POST'])
def edit():
    id = request.form['id']
    date = request.form['date']
    name = request.form['name']
    amount = request.form['amount']
    category = request.form['category']

    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.name = name
    expense.amount = amount
    expense.category = category

    db.session.commit()
    return redirect("/expenses")


@app.route('/addview', methods=['GET', 'POST'])
def addview():
    if request.method == "GET":
        expenses = Expense.query.all()
        total = 0
        t_household = 0
        t_entertainment = 0
        t_education = 0
        t_health = 0
        t_eat = 0
        t_other = 0
        for expense in expenses:
            total += expense.amount
            if expense.category == 'Household':
                t_household += expense.amount

            elif expense.category == 'Entertainment':
                t_entertainment += expense.amount

            elif expense.category == 'Education':
                t_education += expense.amount

            elif expense.category == 'Health':
                t_health += expense.amount

            elif expense.category == 'Eat Outside':
                t_eat += expense.amount

            elif expense.category == 'Other':
                t_other += expense.amount

    elif request.method == "POST":
        date = request.form['date']
        name = request.form['name']
        amount = request.form['amount']
        category = request.form['category']
        expense = Expense(date=date, name=name,
                          amount=amount, category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect("/addview")
    return render_template("addview.html", expenses=expenses, total=total, t_household=t_household, t_entertainment=t_entertainment, t_education=t_education, t_health=t_health, t_eat=t_eat, t_other=t_other)


if __name__ == "__main__":
    app.run(debug=True)
