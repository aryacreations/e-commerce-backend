# E-Commerce Backend System

A scalable backend system for a mini e-commerce platform built with Python, FastAPI, MongoDB, and Prisma.

## Features

- **Authentication System**: JWT-based user registration and login with password hashing
- **Product Management**: CRUD operations for products with search, filter, and sort capabilities
- **Shopping Cart**: User-specific cart management with persistent storage
- **Order Processing**: Checkout flow with order history and item snapshots
- **Clean Architecture**: Layered design with separation of concerns
- **API Documentation**: Auto-generated Swagger UI documentation

## Tech Stack

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Database**: MongoDB
- **ORM**: Prisma (prisma-client-py)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest

## Project Structure

```
e-commerce-backend/
├── src/
│   ├── api/
│   │   ├── deps.py              # Dependency injection
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── products.py      # Product endpoints
│   │       ├── cart.py          # Cart endpoints
│   │       └── orders.py        # Order endpoints
│   ├── core/
│   │   ├── config.py            # Settings and configuration
│   │   ├── security.py          # Password hashing, JWT
│   │   └── database.py          # Database connection
│   ├── schemas/
│   │   ├── user.py              # User schemas
│   │   ├── product.py           # Product schemas
│   │   ├── cart.py              # Cart schemas
│   │   ├── order.py             # Order schemas
│   │   └── token.py             # Token schemas
│   ├── services/
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── product_service.py   # Product business logic
│   │   ├── cart_service.py      # Cart business logic
│   │   └── order_service.py     # Order business logic
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── cart_repository.py
│   │   └── order_repository.py
│   ├── middlewares/
│   │   └── error_handler.py     # Global error handling
│   ├── utils/
│   │   └── pagination.py        # Pagination utilities
│   └── main.py                  # Application entry point
├── prisma/
│   └── schema.prisma            # Prisma schema definition
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── .env                         # Environment variables
├── .env.example                 # Example environment variables
├── requirements.txt             # Python dependencies
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account or local MongoDB instance
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/aryacreations/e-commerce-backend.git
   cd e-commerce-backend
   ```

2. **Create and activate virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` to `.env` and update with your values:

   ```env
   APP_NAME=E-Commerce Backend
   DEBUG=True
   DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/dbname
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEFAULT_PAGE_SIZE=20
   MAX_PAGE_SIZE=100
   ```

5. **Generate Prisma client**

   ```bash
   prisma generate
   ```

6. **Run database migrations** (if needed)
   ```bash
   prisma db push
   ```

### Running the Application

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Environment Variables

| Variable                      | Description               | Default            |
| ----------------------------- | ------------------------- | ------------------ |
| `APP_NAME`                    | Application name          | E-Commerce Backend |
| `DEBUG`                       | Debug mode                | True               |
| `DATABASE_URL`                | MongoDB connection string | Required           |
| `SECRET_KEY`                  | JWT secret key            | Required           |
| `ALGORITHM`                   | JWT algorithm             | HS256              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time     | 30                 |
| `DEFAULT_PAGE_SIZE`           | Default pagination size   | 20                 |
| `MAX_PAGE_SIZE`               | Maximum pagination size   | 100                |

## API Documentation

### Authentication Endpoints

#### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Product Endpoints

#### Create Product (Protected)

```http
POST /api/v1/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics",
  "imageUrl": "https://example.com/image.jpg"
}
```

#### Get All Products

```http
GET /api/v1/products?page=1&page_size=20&search=laptop&category=Electronics&sort=price_asc
```

#### Get Single Product

```http
GET /api/v1/products/{product_id}
```

#### Update Product (Protected)

```http
PUT /api/v1/products/{product_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "price": 89.99
}
```

#### Delete Product (Protected)

```http
DELETE /api/v1/products/{product_id}
Authorization: Bearer <token>
```

### Cart Endpoints

#### Add to Cart (Protected)

```http
POST /api/v1/cart/items
Authorization: Bearer <token>
Content-Type: application/json

{
  "productId": "product_id_here",
  "quantity": 2
}
```

#### Get Cart (Protected)

```http
GET /api/v1/cart
Authorization: Bearer <token>
```

#### Update Cart Item (Protected)

```http
PUT /api/v1/cart/items/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 5
}
```

#### Remove from Cart (Protected)

```http
DELETE /api/v1/cart/items/{item_id}
Authorization: Bearer <token>
```

### Order Endpoints

#### Create Order (Protected)

```http
POST /api/v1/orders
Authorization: Bearer <token>
```

#### Get Order History (Protected)

```http
GET /api/v1/orders
Authorization: Bearer <token>
```

#### Get Specific Order (Protected)

```http
GET /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

## Database Schema

### User

- `id`: ObjectId (Primary Key)
- `email`: String (Unique)
- `hashedPassword`: String
- `createdAt`: DateTime

### Product

- `id`: ObjectId (Primary Key)
- `title`: String
- `description`: String
- `price`: Float
- `category`: String
- `imageUrl`: String
- `createdAt`: DateTime
- `updatedAt`: DateTime

### Cart

- `id`: ObjectId (Primary Key)
- `userId`: ObjectId (Foreign Key, Unique)
- `createdAt`: DateTime
- `updatedAt`: DateTime

### CartItem

- `id`: ObjectId (Primary Key)
- `cartId`: ObjectId (Foreign Key)
- `productId`: ObjectId (Foreign Key)
- `quantity`: Integer
- Unique constraint on (cartId, productId)

### Order

- `id`: ObjectId (Primary Key)
- `userId`: ObjectId (Foreign Key)
- `totalPrice`: Float
- `status`: String (default: "pending")
- `createdAt`: DateTime

### OrderItem

- `id`: ObjectId (Primary Key)
- `orderId`: ObjectId (Foreign Key)
- `productId`: ObjectId (Foreign Key)
- `productTitle`: String (snapshot)
- `productPrice`: Float (snapshot)
- `quantity`: Integer

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=src tests/
```

## Error Handling

The API returns consistent error responses:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected endpoints with bearer token
- Input validation with Pydantic
- CORS middleware configuration
- Environment-based configuration

## Development

### Code Style

The project follows clean architecture principles:

- **API Layer**: Route handlers
- **Service Layer**: Business logic
- **Repository Layer**: Data access
- **Schema Layer**: Request/response validation

### Adding New Features

1. Define Prisma model in `prisma/schema.prisma`
2. Create Pydantic schemas in `src/schemas/`
3. Implement repository in `src/repositories/`
4. Implement service in `src/services/`
5. Create API endpoints in `src/api/v1/`
6. Write tests in `tests/`

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Set up MongoDB Atlas with proper security
- [ ] Enable MongoDB connection pooling
- [ ] Set up logging and monitoring
- [ ] Use environment variables for sensitive data
- [ ] Run `prisma generate` before deployment

### Deployment Platforms

- **Heroku**: Use Procfile with `web: uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- **AWS/GCP/Azure**: Deploy with Docker or serverless functions
- **Railway/Render**: Direct deployment from GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact: [your-email@example.com]

## Acknowledgments

- FastAPI for the excellent web framework
- Prisma for the modern ORM
- MongoDB for the flexible databa

## Fro

ntend

A simple Streamlit-based frontend is included in the `frontend/` directory.

### Running the Frontend

1. Install frontend dependencies:

   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. Make sure the backend is running:

   ```bash
   uvicorn src.main:app --reload
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Access at `http://localhost:8501`

### Frontend Features

- User registration and login
- Product browsing with search, filter, and sort
- Shopping cart management
- Order placement and history
- Product management (add new products)
