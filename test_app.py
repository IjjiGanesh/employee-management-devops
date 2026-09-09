import os
import pytest

from app import app
from database import init_db, get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    if os.path.exists("employees.db"):
        os.remove("employees.db")

    init_db()

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_employee(client):
    response = client.post(
        "/add",
        data={
            "name": "Test Employee",
            "email": "test@example.com",
            "department": "IT",
            "salary": "50000"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    connection = get_db_connection()
    employee = connection.execute(
        "SELECT * FROM employees WHERE email = ?",
        ("test@example.com",)
    ).fetchone()
    connection.close()

    assert employee is not None
    assert employee["name"] == "Test Employee"


def test_delete_employee(client):
    client.post(
        "/add",
        data={
            "name": "Delete Test",
            "email": "delete@example.com",
            "department": "HR",
            "salary": "40000"
        }
    )

    connection = get_db_connection()
    employee = connection.execute(
        "SELECT * FROM employees WHERE email = ?",
        ("delete@example.com",)
    ).fetchone()
    connection.close()

    assert employee is not None

    response = client.post(
        f"/delete/{employee['id']}",
        follow_redirects=True
    )

    assert response.status_code == 200

    connection = get_db_connection()
    deleted_employee = connection.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee["id"],)
    ).fetchone()
    connection.close()

    assert deleted_employee is None
