import pytest
from fastapi.testclient import TestClient


def setup_user_and_product(client: TestClient):
    """Helper to setup user and product for cart tests."""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={"email": "cartuser@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "cartuser@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Create a product
    product_response = client.post(
        "/api/v1/products",
        json={
            "title": "Cart Test Product",
            "description": "For cart testing",
            "price": 50.00,
            "category": "Test",
            "imageUrl": "https://example.com/test.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = product_response.json()["id"]
    
    return token, product_id


def test_add_to_cart_success(client: TestClient):
    """Test adding item to cart."""
    token, product_id = setup_user_and_product(client)
    
    response = client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["productId"] == product_id
    assert data["quantity"] == 2


def test_add_existing_product_updates_quantity(client: TestClient):
    """Test adding existing product updates quantity."""
    token, product_id = setup_user_and_product(client)
    
    # Add first time
    client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Add again
    response = client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 5  # 2 + 3


def test_add_nonexistent_product(client: TestClient):
    """Test adding non-existent product to cart."""
    token, _ = setup_user_and_product(client)
    
    response = client.post(
        "/api/v1/cart/items",
        json={"productId": "nonexistent123", "quantity": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400


def test_get_cart(client: TestClient):
    """Test getting user cart."""
    token, product_id = setup_user_and_product(client)
    
    # Add item to cart
    client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get cart
    response = client.get(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert "totalPrice" in data


def test_get_empty_cart(client: TestClient):
    """Test getting empty cart."""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={"email": "emptycart@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "emptycart@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0


def test_update_cart_item_quantity(client: TestClient):
    """Test updating cart item quantity."""
    token, product_id = setup_user_and_product(client)
    
    # Add item
    add_response = client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = add_response.json()["id"]
    
    # Update quantity
    response = client.put(
        f"/api/v1/cart/items/{item_id}",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5


def test_remove_cart_item(client: TestClient):
    """Test removing item from cart."""
    token, product_id = setup_user_and_product(client)
    
    # Add item
    add_response = client.post(
        "/api/v1/cart/items",
        json={"productId": product_id, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = add_response.json()["id"]
    
    # Remove item
    response = client.delete(
        f"/api/v1/cart/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204


def test_unauthorized_cart_access(client: TestClient):
    """Test accessing cart without authentication."""
    response = client.get("/api/v1/cart")
    assert response.status_code == 403
