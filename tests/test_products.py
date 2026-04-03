import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient) -> str:
    """Helper to get authentication token."""
    client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "password123"}
    )
    return response.json()["access_token"]


def test_create_product_success(client: TestClient):
    """Test creating product with valid data."""
    token = get_auth_token(client)
    
    response = client.post(
        "/api/v1/products",
        json={
            "title": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "category": "Electronics",
            "imageUrl": "https://example.com/image.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["price"] == 99.99


def test_create_product_invalid_price(client: TestClient):
    """Test creating product with invalid price."""
    token = get_auth_token(client)
    
    response = client.post(
        "/api/v1/products",
        json={
            "title": "Test Product",
            "description": "Test Description",
            "price": -10,
            "category": "Electronics",
            "imageUrl": "https://example.com/image.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422


def test_get_all_products(client: TestClient):
    """Test getting all products with pagination."""
    response = client.get("/api/v1/products?page=1&page_size=20")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "page" in data


def test_search_products(client: TestClient):
    """Test searching products by name."""
    token = get_auth_token(client)
    
    # Create a product
    client.post(
        "/api/v1/products",
        json={
            "title": "Laptop Computer",
            "description": "High performance laptop",
            "price": 999.99,
            "category": "Electronics",
            "imageUrl": "https://example.com/laptop.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Search for it
    response = client.get("/api/v1/products?search=Laptop")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0


def test_filter_products_by_category(client: TestClient):
    """Test filtering products by category."""
    response = client.get("/api/v1/products?category=Electronics")
    assert response.status_code == 200


def test_sort_products_by_price(client: TestClient):
    """Test sorting products by price."""
    response = client.get("/api/v1/products?sort=price_asc")
    assert response.status_code == 200
    
    response = client.get("/api/v1/products?sort=price_desc")
    assert response.status_code == 200


def test_get_nonexistent_product(client: TestClient):
    """Test getting non-existent product."""
    response = client.get("/api/v1/products/nonexistent123")
    assert response.status_code == 404


def test_update_product(client: TestClient):
    """Test updating a product."""
    token = get_auth_token(client)
    
    # Create product
    create_response = client.post(
        "/api/v1/products",
        json={
            "title": "Original Title",
            "description": "Original Description",
            "price": 50.00,
            "category": "Books",
            "imageUrl": "https://example.com/book.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_response.json()["id"]
    
    # Update product
    response = client.put(
        f"/api/v1/products/{product_id}",
        json={"title": "Updated Title", "price": 60.00},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["price"] == 60.00


def test_delete_product(client: TestClient):
    """Test deleting a product."""
    token = get_auth_token(client)
    
    # Create product
    create_response = client.post(
        "/api/v1/products",
        json={
            "title": "To Delete",
            "description": "Will be deleted",
            "price": 25.00,
            "category": "Test",
            "imageUrl": "https://example.com/test.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_response.json()["id"]
    
    # Delete product
    response = client.delete(
        f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
