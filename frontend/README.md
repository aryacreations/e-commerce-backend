# E-Commerce Frontend (Streamlit)

A simple Streamlit-based frontend for the E-Commerce Backend API.

## Features

- **User Authentication**: Register and login
- **Product Browsing**: View, search, filter, and sort products
- **Shopping Cart**: Add items, update quantities, remove items
- **Checkout**: Place orders from cart
- **Order History**: View past orders
- **Product Management**: Add new products (admin feature)

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure the backend is running**

   ```bash
   # In the root directory
   uvicorn src.main:app --reload
   ```

3. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`

## Usage

### Register/Login

- Use the sidebar to register a new account or login
- Email format: `user@example.com`
- Password: minimum 6 characters

### Browse Products

- View all products in the Products tab
- Use search to find products by name
- Filter by category
- Sort by price (ascending/descending)

### Shopping Cart

- Add products to cart (must be logged in)
- Update quantities
- Remove items
- View total price
- Checkout to place order

### Orders

- View order history
- See order details including items and total

### Add Products

- Add new products to the store
- Requires authentication
- Fill in product details and submit

## API Configuration

The frontend connects to the backend API at `http://localhost:8000/api/v1`

To change the API URL, edit the `API_BASE_URL` variable in `app.py`.

## Screenshots

### Products Page

Browse and search products with filtering and sorting options.

### Cart Page

Manage your shopping cart and proceed to checkout.

### Orders Page

View your order history and details.

## Notes

- Make sure the backend server is running before starting the frontend
- The app uses session state to maintain login status
- All API calls are made to the FastAPI backend
