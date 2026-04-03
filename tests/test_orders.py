import pytest
from fastapi.testclient import TestClient


def setup_cart_with_items(client: TestClient):
    """Helper to setup user with cart items."""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={"email": "orderuser@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "orderuser@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Create products
    product1 = client.post(
        "/api/v1/products",
        json={
            "title": "Product 1",
            "description": "First product",
            "price": 50.00,
            "category": "Test",
            "imageUrl": "https://example.com/p1.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    product2 = client.post(
        "/api/v1/products",
        json={
            "title": "Product 2",
            "description": "Second product",
            "price": 75.00,
            "category": "Test",
            "imageUrl": "https://example.com/p2.jpg"
        },
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    # Add to cart
    client.post(
        "/api/v1/cart/items",
        json={"productId": product1["id"], "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        "/api/v1/cart/items",
        json={"productId": product2["id"], "quantity": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return token


def test_create_order_success(client: TestClient):
    """Test creating order from cart."""
    token = setup_cart_with_items(client)
    
    response = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["totalPrice"] > 0
    assert len(data["items"]) == 2


def test_create_order_empty_cart(client: TestClient):
    """Test creating order with empty cart."""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={"email": "emptycartorder@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "emptycartorder@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    response = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "empty cart" in response.json()["detail"].lower()


def test_cart_cleared_after_order(client: TestClient):
    """Test that cart is cleared after order creation."""
    token = setup_cart_with_items(client)
    
    # Create order
    client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Check cart is empty
    cart_response = client.get(
        "/api/v1/cart",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert cart_response.status_code == 200
    cart_data = cart_response.json()
    assert len(cart_data["items"]) == 0


def test_get_user_orders(client: TestClient):
    """Test getting user order history."""
    token = setup_cart_with_items(client)
    
    # Create order
    client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get orders
    response = client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "items" in data[0]


def test_get_specific_order(client: TestClient):
    """Test getting specific order."""
    token = setup_cart_with_items(client)
    
    # Create order
    order_response = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    order_id = order_response.json()["id"]
    
    # Get specific order
    response = client.get(
        f"/api/v1/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


def test_order_items_snapshot(client: TestClient):
    """Test that order items are snapshots of products."""
    token = setup_cart_with_items(client)
    
    # Create order
    order_response = client.post(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    order_data = order_response.json()
    
    # Verify order items have product snapshots
    for item in order_data["items"]:
        assert "productTitle" in item
        assert "productPrice" in item
        assert item["productTitle"] != ""
        assert item["productPrice"] > 0
