import sqlite3

DATABASE = "employees.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def get_all_employees():
    connection = get_db_connection()

    employees = connection.execute(
        "SELECT * FROM employees ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return employees


def add_employee(name, email, department, salary):
    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO employees (name, email, department, salary)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, department, salary)
        )

        connection.commit()

    finally:
        connection.close()


def delete_employee(employee_id):
    connection = get_db_connection()

    try:
        connection.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

        connection.commit()

    finally:
        connection.close()