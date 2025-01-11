import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_user(client):
    response = client.post("/api/users", json={"username": "john", "email": "john@example.com"})
    assert response.status_code == 201

def test_get_user(client):
    response = client.get("/api/users/1")
    assert response.status_code in [200, 404]
