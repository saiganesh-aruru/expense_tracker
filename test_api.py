from fastapi.testclient import TestClient
from api import app
import api
import pytest

client = TestClient(app)

@pytest.fixture
def test_storage(tmp_path):
    original_file = api.STORAGE_FILE
    api.STORAGE_FILE = str(tmp_path / "test_expenses.json")

    yield

    api.STORAGE_FILE = original_file

import api
import pytest

from fastapi.testclient import TestClient

client = TestClient(api.app)


@pytest.fixture
def test_storage(tmp_path):
    original_file = api.STORAGE_FILE
    api.STORAGE_FILE = str(tmp_path / "test_expenses.json")

    yield

    api.STORAGE_FILE = original_file


# ---------- GET ----------

def test_get_expenses(test_storage):
    response = client.get("/expenses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_expense(test_storage):
    create_response = client.post(
        "/expenses",
        json={
            "name": "Test Expense",
            "amount": 100
        }
    )

    expense_id = create_response.json()["id"]

    response = client.get(f"/expenses/{expense_id}")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["id"] == expense_id
    assert data["name"] == "Test Expense"
    assert data["amount"] == 100


def test_get_expense_not_found(test_storage):
    response = client.get("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


# ---------- POST ----------

def test_create_expense(test_storage):
    response = client.post(
        "/expenses",
        json={
            "name": "Food",
            "amount": 250
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Food"
    assert data["amount"] == 250
    assert "id" in data


def test_create_expense_invalid_amount(test_storage):
    response = client.post(
        "/expenses",
        json={
            "name": "Food",
            "amount": 0
        }
    )

    assert response.status_code == 422


# ---------- PATCH ----------

def test_update_expense(test_storage):
    create_response = client.post(
        "/expenses",
        json={
            "name": "Food",
            "amount": 250
        }
    )

    expense_id = create_response.json()["id"]

    response = client.patch(
        f"/expenses/{expense_id}",
        json={
            "amount": 300
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == expense_id
    assert data["name"] == "Food"
    assert data["amount"] == 300


def test_update_missing_expense(test_storage):
    response = client.patch(
        "/expenses/999999",
        json={
            "amount": 500
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


# ---------- PUT ----------

def test_replace_expense(test_storage):
    create_response = client.post(
        "/expenses",
        json={
            "name": "Food",
            "amount": 250
        }
    )

    expense_id = create_response.json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={
            "name": "Travel",
            "amount": 500
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == expense_id
    assert data["name"] == "Travel"
    assert data["amount"] == 500


def test_replace_missing_expense(test_storage):
    response = client.put(
        "/expenses/999999",
        json={
            "name": "Food",
            "amount": 500
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


# ---------- DELETE ----------

def test_delete_expense(test_storage):
    create_response = client.post(
        "/expenses",
        json={
            "name": "Food",
            "amount": 250
        }
    )

    expense_id = create_response.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Expense deleted"

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 404


def test_delete_missing_expense(test_storage):
    response = client.delete("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"