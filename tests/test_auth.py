"""
Test authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, db):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_login_access_token(client: TestClient):
    """Test user login."""
    # First register a user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_register_duplicate_email(client: TestClient):
    """Test registration with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # Register first user
    response1 = client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 200
    
    # Try to register with same email
    user_data["username"] = "testuser2"
    response2 = client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == 400
