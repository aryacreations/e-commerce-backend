import pytest
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    """Test registration with duplicate email."""
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    
    # Second registration with same email
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_register_invalid_email(client: TestClient):
    """Test registration with invalid email format."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "invalid-email", "password": "password123"}
    )
    assert response.status_code == 422


def test_register_short_password(client: TestClient):
    """Test registration with short password."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "123"}
    )
    assert response.status_code == 422


def test_login_success(client: TestClient):
    """Test successful login."""
    # Register user first
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_access_protected_without_token(client: TestClient):
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/cart")
    assert response.status_code == 403
