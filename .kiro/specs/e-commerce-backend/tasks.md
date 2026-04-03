# Implementation Plan

- [x] 1. Set up project structure and dependencies

  - Create project directory structure (src/, prisma/, tests/)
  - Initialize Python virtual environment
  - Create requirements.txt with FastAPI, Prisma, passlib, python-jose, pymongo dependencies
  - Create .env.example file with required environment variables
  - Create .gitignore file
  - _Requirements: 7.1, 7.2_

- [x] 2. Configure Prisma schema and database connection

  - Create prisma/schema.prisma with MongoDB datasource configuration
  - Define User model in Prisma schema
  - Define Product model in Prisma schema
  - Define Cart and CartItem models in Prisma schema
  - Define Order and OrderItem models in Prisma schema
  - Create .env file with MongoDB connection string
  - Generate Prisma client
  - _Requirements: 7.1, 7.2, 7.4_

- [x] 3. Implement core configuration and security utilities

  - Create src/core/config.py with Settings class using Pydantic BaseSettings
  - Create src/core/security.py with password hashing functions (hash_password, verify_password)
  - Implement JWT token creation and validation functions in security.py
  - Create src/core/database.py with Prisma client initialization
  - _Requirements: 1.1, 1.5, 7.6_

- [x] 4. Create Pydantic schemas for request/response validation

  - Create src/schemas/token.py with Token and TokenData schemas
  - Create src/schemas/user.py with UserCreate, UserLogin, UserResponse schemas
  - Create src/schemas/product.py with ProductCreate, ProductUpdate, ProductResponse schemas
  - Create src/schemas/cart.py with CartItemCreate, CartItemUpdate, CartResponse schemas
  - Create src/schemas/order.py with OrderCreate, OrderResponse schemas
  - Add validators for email format, positive prices, and quantity
  - _Requirements: 6.1, 7.4_

- [x] 5. Implement user repository layer

  - Create src/repositories/user_repository.py
  - Implement create_user function using Prisma client
  - Implement get_user_by_email function
  - Implement get_user_by_id function
  - Add error handling for database operations
  - _Requirements: 1.1, 1.2, 7.3_

- [x] 6. Implement authentication service layer

  - Create src/services/auth_service.py
  - Implement register_user function with duplicate email check
  - Implement authenticate_user function with password verification
  - Implement get_current_user function with JWT token validation
  - Add validation for email format and password strength
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

- [x] 7. Create authentication API endpoints

  - Create src/api/deps.py with get_current_user dependency
  - Create src/api/v1/auth.py with router
  - Implement POST /auth/register endpoint
  - Implement POST /auth/login endpoint
  - Add error handling for duplicate users and invalid credentials
  - Test endpoints return proper status codes and JWT tokens
  - _Requirements: 1.1, 1.2, 1.5, 1.6, 1.7, 1.8_

- [x] 8. Implement product repository layer

  - Create src/repositories/product_repository.py
  - Implement create_product function
  - Implement get_products function with pagination, search, filter, and sort
  - Implement get_product_by_id function
  - Implement update_product function
  - Implement delete_product function
  - _Requirements: 2.1, 2.2, 2.3, 2.5, 2.6, 7.3_

- [x] 9. Implement product service layer

  - Create src/services/product_service.py
  - Implement create_product with validation
  - Implement get_products with search (contains), filter (category), and sort (price)
  - Implement get_product_by_id with not found handling
  - Implement update_product with validation
  - Implement delete_product
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 10. Create product management API endpoints

  - Create src/api/v1/products.py with router
  - Implement POST /products endpoint (protected, admin only for bonus)
  - Implement GET /products endpoint with query parameters (search, category, sort, page, page_size)
  - Implement GET /products/{product_id} endpoint
  - Implement PUT /products/{product_id} endpoint (protected)
  - Implement DELETE /products/{product_id} endpoint (protected)
  - Add proper error responses for not found and validation errors
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 11. Implement cart repository layer

  - Create src/repositories/cart_repository.py
  - Implement get_or_create_cart function for user
  - Implement add_cart_item function with upsert logic for existing products
  - Implement get_cart_items function with product details
  - Implement update_cart_item_quantity function
  - Implement remove_cart_item function
  - Implement clear_cart function
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 7.3_

- [x] 12. Implement cart service layer

  - Create src/services/cart_service.py
  - Implement add_to_cart with product existence validation
  - Implement remove_from_cart with ownership validation
  - Implement update_cart_item with quantity validation
  - Implement get_user_cart with total price calculation
  - Implement clear_cart function
  - Add error handling for non-existent products and unauthorized access
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

- [x] 13. Create cart management API endpoints

  - Create src/api/v1/cart.py with router
  - Implement POST /cart/items endpoint (protected) to add items
  - Implement GET /cart endpoint (protected) to get user cart
  - Implement PUT /cart/items/{item_id} endpoint (protected) to update quantity
  - Implement DELETE /cart/items/{item_id} endpoint (protected) to remove item
  - Add authentication dependency to all endpoints
  - Handle empty cart scenario gracefully
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

- [x] 14. Implement order repository layer

  - Create src/repositories/order_repository.py
  - Implement create_order function with order items
  - Implement get_user_orders function
  - Implement get_order_by_id function with user ownership check
  - _Requirements: 5.1, 5.4, 5.6, 7.3_

- [x] 15. Implement order service layer

  - Create src/services/order_service.py
  - Implement create_order function that validates non-empty cart
  - Copy cart items to order items with product snapshots (title, price)
  - Calculate and store total price
  - Clear cart after order creation
  - Implement get_user_orders function
  - Implement get_order_by_id with ownership validation
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 16. Create order management API endpoints

  - Create src/api/v1/orders.py with router
  - Implement POST /orders endpoint (protected) to create order from cart
  - Implement GET /orders endpoint (protected) to get user order history
  - Implement GET /orders/{order_id} endpoint (protected) to get specific order
  - Add error handling for empty cart and unauthorized access
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_

- [x] 17. Implement global error handling middleware

  - Create src/middlewares/error_handler.py
  - Define custom exception classes (NotFoundException, UnauthorizedException, etc.)
  - Create exception handlers for each custom exception type
  - Map exceptions to appropriate HTTP status codes
  - Return consistent error response format
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [x] 18. Create main application entry point

  - Create src/main.py with FastAPI app initialization
  - Register all routers (auth, products, cart, orders)
  - Add CORS middleware configuration
  - Add global error handler middleware
  - Create /health endpoint for monitoring
  - Configure Prisma client lifecycle (connect on startup, disconnect on shutdown)
  - _Requirements: 7.1, 7.2, 7.6_

- [x] 19. Create utility functions

  - Create src/utils/pagination.py with pagination helper functions
  - Implement calculate_total_pages function
  - Implement validate_pagination_params function
  - _Requirements: 3.5, 7.2_

- [x] 20. Write unit tests for authentication

  - Create tests/conftest.py with test fixtures (test database, test client)
  - Create tests/test_auth.py
  - Write test for successful user registration
  - Write test for duplicate email registration
  - Write test for invalid email format
  - Write test for successful login
  - Write test for invalid credentials
  - Write test for accessing protected endpoint without token
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_

- [x] 21. Write unit tests for product management

  - Create tests/test_products.py
  - Write test for creating product with valid data
  - Write test for creating product with invalid data
  - Write test for getting all products with pagination
  - Write test for searching products by name
  - Write test for filtering products by category
  - Write test for sorting products by price
  - Write test for getting non-existent product
  - Write test for updating and deleting products
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 22. Write unit tests for cart management

  - Create tests/test_cart.py
  - Write test for adding item to cart
  - Write test for adding existing product (quantity update)
  - Write test for adding non-existent product
  - Write test for removing item from cart
  - Write test for updating cart item quantity
  - Write test for getting empty cart
  - Write test for unauthorized cart access
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

- [x] 23. Write unit tests for order management

  - Create tests/test_orders.py
  - Write test for creating order from cart
  - Write test for creating order with empty cart
  - Write test for verifying cart is cleared after order
  - Write test for getting user order history
  - Write test for getting specific order
  - Write test for accessing another user's order
  - Write test for order items snapshot (product changes don't affect order)
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 24. Create project documentation

  - Create README.md with project overview
  - Document setup instructions (virtual environment, dependencies, Prisma)
  - Document environment variables required
  - Document API endpoints with examples (or reference Swagger UI)
  - Document database schema
  - Add instructions for running tests
  - Add instructions for running the application
  - _Requirements: 7.1, 7.2_

- [ ] 25. Optional: Implement wishlist feature

  - Create Wishlist and WishlistItem models in Prisma schema
  - Create wishlist repository, service, and API endpoints
  - Write tests for wishlist functionality
  - _Requirements: 8.1, 8.2_

- [ ] 26. Optional: Implement product reviews feature

  - Create Review model in Prisma schema
  - Create review repository, service, and API endpoints
  - Write tests for review functionality
  - _Requirements: 8.3_

- [ ] 27. Optional: Implement role-based access control
  - Add role field to User model in Prisma schema
  - Create admin-only decorator/dependency
  - Protect admin endpoints (create/update/delete products)
  - Write tests for role-based access
  - _Requirements: 8.4_
