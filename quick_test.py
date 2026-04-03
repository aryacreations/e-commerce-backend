"""Quick manual test"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing API...")
print("="*50)

# Test 1: Health check
print("\n1. Health Check:")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

# Test 2: Register user with short password
print("\n2. Register User (short password):")
user_data = {
    "email": "quick@test.com",
    "password": "test12"
}
response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text}")

# Test 3: Login
if response.status_code == 201:
    print("\n3. Login:")
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=user_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"   Token: {token[:30]}...")
        
        # Test 4: Create product
        print("\n4. Create Product:")
        product = {
            "title": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "category": "Test",
            "imageUrl": "https://example.com/test.jpg"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/api/v1/products", json=product, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        if response.status_code == 201:
            product_id = response.json()['id']
            
            # Test 5: Get products
            print("\n5. Get All Products:")
            response = requests.get(f"{BASE_URL}/api/v1/products")
            print(f"   Status: {response.status_code}")
            products = response.json()
            print(f"   Total products: {products['total']}")
            
            # Test 6: Add to cart
            print("\n6. Add to Cart:")
            cart_item = {"productId": product_id, "quantity": 2}
            response = requests.post(f"{BASE_URL}/api/v1/cart/items", json=cart_item, headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
            # Test 7: Get cart
            print("\n7. Get Cart:")
            response = requests.get(f"{BASE_URL}/api/v1/cart", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                cart = response.json()
                print(f"   Items: {len(cart['items'])}, Total: ${cart['totalPrice']}")
            
            # Test 8: Create order
            print("\n8. Create Order:")
            response = requests.post(f"{BASE_URL}/api/v1/orders", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                order = response.json()
                print(f"   Order ID: {order['id']}, Total: ${order['totalPrice']}")
            else:
                print(f"   Response: {response.text}")

print("\n" + "="*50)
print("Testing complete!")
