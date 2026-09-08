from flask import Flask, render_template, request, redirect, url_for

from database import (
    init_db,
    get_all_employees,
    add_employee,
    delete_employee
)

app = Flask(__name__)


@app.route("/")
def home():
    employees = get_all_employees()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    salary = request.form["salary"]

    add_employee(name, email, department, salary)

    return redirect(url_for("home"))


@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete(employee_id):
    delete_employee(employee_id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
