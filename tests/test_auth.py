import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import authenticate_user

@pytest.fixture
def client():
    return TestClient(app)

def test_authenticate_user(client):
    # Test with valid credentials
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # Test with invalid credentials
    response = client.post("/token", data={
        "username": "invaliduser",
        "password": "invalidpassword"
    })
    assert response.status_code == 401
