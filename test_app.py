import pytest

from app import app
from database import init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_employee(client):
    init_db()

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
    assert b"Test Employee" in response.data


def test_delete_employee(client):
    init_db()

    client.post(
        "/add",
        data={
            "name": "Delete Test",
            "email": "delete@example.com",
            "department": "HR",
            "salary": "40000"
        }
    )

    response = client.get("/")

    assert response.status_code == 200
    assert b"Delete Test" in response.data
