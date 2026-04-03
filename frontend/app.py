import streamlit as st
import requests
import json

# API Base URL
API_BASE_URL = "http://localhost:8000/api/v1"

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'cart_count' not in st.session_state:
    st.session_state.cart_count = 0

# Helper function to get headers
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

# Page config
st.set_page_config(page_title="E-Commerce App", page_icon="🛒", layout="wide")

# Sidebar for authentication
with st.sidebar:
    st.title("🛒 E-Commerce")
    
    if st.session_state.token:
        st.success(f"Logged in as: {st.session_state.user_email}")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user_email = None
            st.session_state.cart_count = 0
            st.rerun()
    else:
        st.subheader("Authentication")
        auth_tab = st.radio("", ["Login", "Register"], horizontal=True)
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if auth_tab == "Register":
            if st.button("Register"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/auth/register",
                        json={"email": email, "password": password}
                    )
                    if response.status_code == 201:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Registration failed')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        else:  # Login
            if st.button("Login"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/auth/login",
                        json={"email": email, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.user_email = email
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Login failed')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Main content
st.title("🛍️ E-Commerce Store")

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏪 Products", "🛒 Cart", "📦 Orders", "➕ Add Product"])

# Tab 1: Products
with tab1:
    st.header("Browse Products")
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search products", "")
    with col2:
        category = st.text_input("📁 Filter by category", "")
    with col3:
        sort = st.selectbox("Sort by", ["", "price_asc", "price_desc"])
    
    # Fetch products
    try:
        params = {"page": 1, "page_size": 20}
        if search:
            params["search"] = search
        if category:
            params["category"] = category
        if sort:
            params["sort"] = sort
        
        response = requests.get(f"{API_BASE_URL}/products", params=params)
        if response.status_code == 200:
            data = response.json()
            products = data.get("data", [])
            
            if products:
                # Display products in grid
                cols = st.columns(3)
                for idx, product in enumerate(products):
                    with cols[idx % 3]:
                        st.image(product["imageUrl"], use_container_width=True)
                        st.subheader(product["title"])
                        st.write(product["description"][:100] + "...")
                        st.write(f"**Price:** ${product['price']:.2f}")
                        st.write(f"**Category:** {product['category']}")
                        
                        if st.session_state.token:
                            quantity = st.number_input(
                                "Quantity",
                                min_value=1,
                                value=1,
                                key=f"qty_{product['id']}"
                            )
                            if st.button("Add to Cart", key=f"add_{product['id']}"):
                                try:
                                    cart_response = requests.post(
                                        f"{API_BASE_URL}/cart/items",
                                        json={"productId": product["id"], "quantity": quantity},
                                        headers=get_headers()
                                    )
                                    if cart_response.status_code == 201:
                                        st.success("Added to cart!")
                                        st.session_state.cart_count += quantity
                                    else:
                                        st.error("Failed to add to cart")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        else:
                            st.info("Login to add to cart")
                        
                        st.divider()
            else:
                st.info("No products found")
        else:
            st.error("Failed to load products")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Tab 2: Cart
with tab2:
    st.header("Shopping Cart")
    
    if not st.session_state.token:
        st.warning("Please login to view your cart")
    else:
        try:
            response = requests.get(f"{API_BASE_URL}/cart", headers=get_headers())
            if response.status_code == 200:
                cart_data = response.json()
                items = cart_data.get("items", [])
                
                if items:
                    for item in items:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**{item['product']['title']}**")
                            st.write(f"${item['product']['price']:.2f}")
                        
                        with col2:
                            new_qty = st.number_input(
                                "Qty",
                                min_value=1,
                                value=item["quantity"],
                                key=f"cart_qty_{item['id']}"
                            )
                            if new_qty != item["quantity"]:
                                if st.button("Update", key=f"update_{item['id']}"):
                                    try:
                                        update_response = requests.put(
                                            f"{API_BASE_URL}/cart/items/{item['id']}",
                                            json={"quantity": new_qty},
                                            headers=get_headers()
                                        )
                                        if update_response.status_code == 200:
                                            st.success("Updated!")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                        
                        with col3:
                            st.write(f"**${item['product']['price'] * item['quantity']:.2f}**")
                        
                        with col4:
                            if st.button("Remove", key=f"remove_{item['id']}"):
                                try:
                                    delete_response = requests.delete(
                                        f"{API_BASE_URL}/cart/items/{item['id']}",
                                        headers=get_headers()
                                    )
                                    if delete_response.status_code == 204:
                                        st.success("Removed!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        
                        st.divider()
                    
                    st.subheader(f"Total: ${cart_data['totalPrice']:.2f}")
                    
                    if st.button("🛍️ Checkout", type="primary"):
                        try:
                            order_response = requests.post(
                                f"{API_BASE_URL}/orders",
                                headers=get_headers()
                            )
                            if order_response.status_code == 201:
                                st.success("Order placed successfully!")
                                st.session_state.cart_count = 0
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("Failed to place order")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.info("Your cart is empty")
            else:
                st.error("Failed to load cart")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Tab 3: Orders
with tab3:
    st.header("Order History")
    
    if not st.session_state.token:
        st.warning("Please login to view your orders")
    else:
        try:
            response = requests.get(f"{API_BASE_URL}/orders", headers=get_headers())
            if response.status_code == 200:
                orders = response.json()
                
                if orders:
                    for order in orders:
                        with st.expander(f"Order #{order['id'][:8]} - ${order['totalPrice']:.2f} - {order['status']}"):
                            st.write(f"**Date:** {order['createdAt']}")
                            st.write(f"**Status:** {order['status']}")
                            st.write(f"**Total:** ${order['totalPrice']:.2f}")
                            
                            st.write("**Items:**")
                            for item in order['items']:
                                st.write(f"- {item['productTitle']} x {item['quantity']} = ${item['productPrice'] * item['quantity']:.2f}")
                else:
                    st.info("No orders yet")
            else:
                st.error("Failed to load orders")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Tab 4: Add Product (Admin)
with tab4:
    st.header("Add New Product")
    
    if not st.session_state.token:
        st.warning("Please login to add products")
    else:
        with st.form("add_product_form"):
            title = st.text_input("Product Title")
            description = st.text_area("Description")
            price = st.number_input("Price", min_value=0.01, step=0.01)
            category = st.text_input("Category")
            image_url = st.text_input("Image URL")
            
            submitted = st.form_submit_button("Add Product")
            
            if submitted:
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/products",
                        json={
                            "title": title,
                            "description": description,
                            "price": price,
                            "category": category,
                            "imageUrl": image_url
                        },
                        headers=get_headers()
                    )
                    if response.status_code == 201:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Failed to add product')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("E-Commerce Backend - Built with FastAPI, MongoDB, and Prisma")
