"""Complete E-Commerce API Testing Script"""
import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = ''
    RED = ''
    YELLOW = ''
    BLUE = ''
    END = ''

def print_step(step_num: int, title: str):
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}STEP {step_num}: {title}{Colors.END}")
    print('='*70)

def print_success(message: str):
    print(f"[OK] {message}")

def print_error(message: str):
    print(f"[ERROR] {message}")

def print_info(message: str):
    print(f"[INFO] {message}")

# Global variable to store auth token
auth_token: Optional[str] = None

def test_step_1_add_sample_products():
    """Step 1: Add sample products to database"""
    print_step(1, "ADD SAMPLE PRODUCTS TO DATABASE")
    
    # First, we need to register and login to get auth token
    print_info("Creating admin user for product creation...")
    
    admin_user = {
        "email": "admin@ecommerce.com",
        "password": "admin123"
    }
    
    # Try to register
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=admin_user)
    if response.status_code == 201:
        print_success("Admin user registered successfully")
    elif response.status_code == 400:
        print_info("Admin user already exists")
    else:
        print_error(f"Registration failed: {response.text}")
        return False
    
    # Login to get token
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=admin_user)
    if response.status_code == 200:
        global auth_token
        auth_token = response.json()['access_token']
        print_success(f"Login successful! Token: {auth_token[:30]}...")
    else:
        print_error(f"Login failed: {response.text}")
        return False
    
    # Sample products to add
    sample_products = [
        {
            "title": "iPhone 15 Pro",
            "description": "Latest Apple smartphone with A17 Pro chip",
            "price": 999.99,
            "category": "Electronics",
            "imageUrl": "https://example.com/iphone15.jpg"
        },
        {
            "title": "Samsung Galaxy S24",
            "description": "Flagship Android phone with AI features",
            "price": 899.99,
            "category": "Electronics",
            "imageUrl": "https://example.com/galaxy-s24.jpg"
        },
        {
            "title": "MacBook Pro 16",
            "description": "Powerful laptop with M3 Max chip",
            "price": 2499.99,
            "category": "Computers",
            "imageUrl": "https://example.com/macbook.jpg"
        },
        {
            "title": "Sony WH-1000XM5",
            "description": "Premium noise-cancelling headphones",
            "price": 399.99,
            "category": "Audio",
            "imageUrl": "https://example.com/sony-headphones.jpg"
        },
        {
            "title": "iPad Air",
            "description": "Versatile tablet with M2 chip",
            "price": 599.99,
            "category": "Tablets",
            "imageUrl": "https://example.com/ipad-air.jpg"
        }
    ]
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    created_products = []
    
    for product in sample_products:
        response = requests.post(f"{BASE_URL}/api/v1/products", json=product, headers=headers)
        if response.status_code == 201:
            created = response.json()
            created_products.append(created)
            print_success(f"Created: {product['title']} - ${product['price']}")
        else:
            print_error(f"Failed to create {product['title']}: {response.text}")
    
    print_info(f"\nTotal products created: {len(created_products)}")
    return len(created_products) > 0

def test_step_2_authentication_flow():
    """Step 2: Test authentication flow"""
    print_step(2, "TEST AUTHENTICATION FLOW")
    
    # Test 1: Register new user
    print_info("Test 2.1: Register new user")
    new_user = {
        "email": f"testuser_{hash('test')}@example.com",
        "password": "secure123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=new_user)
    if response.status_code == 201:
        user_data = response.json()
        print_success(f"User registered: {user_data['email']}")
    else:
        print_error(f"Registration failed: {response.text}")
        return False
    
    # Test 2: Login with correct credentials
    print_info("\nTest 2.2: Login with correct credentials")
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=new_user)
    if response.status_code == 200:
        token_data = response.json()
        user_token = token_data['access_token']
        print_success(f"Login successful! Token type: {token_data['token_type']}")
        print_info(f"Access token: {user_token[:50]}...")
    else:
        print_error(f"Login failed: {response.text}")
        return False
    
    # Test 3: Login with wrong password
    print_info("\nTest 2.3: Login with wrong password (should fail)")
    wrong_creds = {
        "email": new_user['email'],
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=wrong_creds)
    if response.status_code == 401:
        print_success("Correctly rejected wrong password")
    else:
        print_error("Should have rejected wrong password")
        return False
    
    # Test 4: Access protected endpoint without token
    print_info("\nTest 2.4: Access protected endpoint without token (should fail)")
    response = requests.get(f"{BASE_URL}/api/v1/cart")
    if response.status_code == 401:
        print_success("Correctly rejected request without token")
    else:
        print_error("Should have rejected request without token")
        return False
    
    # Test 5: Access protected endpoint with token
    print_info("\nTest 2.5: Access protected endpoint with valid token")
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{BASE_URL}/api/v1/cart", headers=headers)
    if response.status_code in [200, 404]:
        print_success("Successfully accessed protected endpoint")
    else:
        print_error(f"Failed to access protected endpoint: {response.text}")
        return False
    
    return True

def test_step_3_cart_and_order():
    """Step 3: Test cart and order functionality"""
    print_step(3, "TEST CART AND ORDER FUNCTIONALITY")
    
    # Create a test user
    print_info("Creating test user for cart/order testing...")
    test_user = {
        "email": "carttest@example.com",
        "password": "cart123"
    }
    
    # Register or login
    requests.post(f"{BASE_URL}/api/v1/auth/register", json=test_user)
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=test_user)
    if response.status_code != 200:
        print_error("Failed to login test user")
        return False
    
    token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get available products
    print_info("\nTest 3.1: Get available products")
    response = requests.get(f"{BASE_URL}/api/v1/products")
    if response.status_code == 200:
        products = response.json()['data']
        if len(products) == 0:
            print_error("No products available. Run step 1 first!")
            return False
        print_success(f"Found {len(products)} products")
        product_id = products[0]['id']
    else:
        print_error("Failed to get products")
        return False
    
    # Test 3.2: Add item to cart
    print_info("\nTest 3.2: Add item to cart")
    cart_item = {
        "productId": product_id,
        "quantity": 2
    }
    response = requests.post(f"{BASE_URL}/api/v1/cart/items", json=cart_item, headers=headers)
    if response.status_code == 201:
        added_item = response.json()
        print_success(f"Added to cart: {added_item['product']['title']} x {added_item['quantity']}")
        cart_item_id = added_item['id']
    else:
        print_error(f"Failed to add to cart: {response.text}")
        return False
    
    # Test 3.3: Get cart
    print_info("\nTest 3.3: Get user cart")
    response = requests.get(f"{BASE_URL}/api/v1/cart", headers=headers)
    if response.status_code == 200:
        cart = response.json()
        print_success(f"Cart retrieved: {len(cart['items'])} items, Total: ${cart['totalPrice']:.2f}")
    else:
        print_error(f"Failed to get cart: {response.text}")
        return False
    
    # Test 3.4: Update cart item quantity
    print_info("\nTest 3.4: Update cart item quantity")
    update_data = {"quantity": 5}
    response = requests.put(f"{BASE_URL}/api/v1/cart/items/{cart_item_id}", 
                           json=update_data, headers=headers)
    if response.status_code == 200:
        updated_item = response.json()
        print_success(f"Updated quantity to: {updated_item['quantity']}")
    else:
        print_error(f"Failed to update cart: {response.text}")
        return False
    
    # Test 3.5: Create order from cart
    print_info("\nTest 3.5: Create order from cart")
    response = requests.post(f"{BASE_URL}/api/v1/orders", headers=headers)
    if response.status_code == 201:
        order = response.json()
        print_success(f"Order created: ID={order['id']}, Total=${order['totalPrice']:.2f}")
        print_success(f"Order items: {len(order['items'])} items")
        order_id = order['id']
    else:
        print_error(f"Failed to create order: {response.text}")
        return False
    
    # Test 3.6: Get order history
    print_info("\nTest 3.6: Get order history")
    response = requests.get(f"{BASE_URL}/api/v1/orders", headers=headers)
    if response.status_code == 200:
        orders = response.json()
        print_success(f"Order history retrieved: {len(orders)} orders")
    else:
        print_error(f"Failed to get order history: {response.text}")
        return False
    
    # Test 3.7: Get specific order
    print_info("\nTest 3.7: Get specific order details")
    response = requests.get(f"{BASE_URL}/api/v1/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        order_detail = response.json()
        print_success(f"Order details: {len(order_detail['items'])} items, Status: {order_detail['status']}")
    else:
        print_error(f"Failed to get order details: {response.text}")
        return False
    
    # Test 3.8: Verify cart is empty after order
    print_info("\nTest 3.8: Verify cart is empty after order creation")
    response = requests.get(f"{BASE_URL}/api/v1/cart", headers=headers)
    if response.status_code == 200:
        cart = response.json()
        if len(cart['items']) == 0:
            print_success("Cart is empty after order creation")
        else:
            print_error("Cart should be empty after order")
            return False
    
    return True

def test_step_4_run_pytest():
    """Step 4: Run pytest test suite"""
    print_step(4, "RUN PYTEST TEST SUITE")
    
    import os
    if os.path.exists("tests"):
        print_info("Running pytest test suite...")
        try:
            import subprocess
            result = subprocess.run(["python", "-m", "pytest", "-v"], capture_output=True, text=True)
            print(result.stdout)
            if result.returncode == 0:
                print_success("All pytest tests passed!")
                return True
            else:
                print_error("Some pytest tests failed")
                print(result.stderr)
                return False
        except Exception as e:
            print_error(f"Failed to run pytest: {str(e)}")
            return False
    else:
        print_info("Tests directory not found. Skipping pytest.")
        return True

def main():
    """Run all test steps"""
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}E-COMMERCE BACKEND - COMPLETE TESTING SUITE{Colors.END}")
    print('='*70)
    print(f"Base URL: {BASE_URL}")
    print('='*70)
    
    results = {}
    
    # Step 1: Add sample products
    results['Step 1: Add Sample Products'] = test_step_1_add_sample_products()
    
    # Step 2: Test authentication
    results['Step 2: Authentication Flow'] = test_step_2_authentication_flow()
    
    # Step 3: Test cart and orders
    results['Step 3: Cart & Order Functionality'] = test_step_3_cart_and_order()
    
    # Step 4: Run pytest
    results['Step 4: Pytest Suite'] = test_step_4_run_pytest()
    
    # Final Summary
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}FINAL TEST SUMMARY{Colors.END}")
    print('='*70)
    
    for test_name, passed in results.items():
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print('='*70)
    if all_passed:
        print(f"[SUCCESS] ALL TESTS PASSED! Your E-Commerce Backend is production-ready!")
    else:
        print(f"[FAILED] Some tests failed. Please review the errors above.")
    print('='*70)
    
    return all_passed

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[WARNING] Testing interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {str(e)}")
