# 🛒 E-Commerce Backend API

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)](https://www.mongodb.com/cloud/atlas)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready, scalable RESTful API for an e-commerce platform built with modern Python technologies. Features include user authentication, product management, shopping cart, and order processing with clean architecture principles.

> **🎥 [Watch the Complete Project Walkthrough & Architecture Explanation Video Here](https://drive.google.com/file/d/1P6nBGOd6Ij5OpGuf9awgQ9ZWZAvq_qyT/view?usp=sharing)**

## 🌟 Key Features

- **🔐 JWT Authentication** - Secure user registration and login with bcrypt password hashing
- **📦 Product Management** - Full CRUD operations with search, filter, and sort capabilities
- **🛒 Shopping Cart** - Persistent cart management with real-time updates
- **📋 Order Processing** - Complete checkout flow with order history and product snapshots
- **🏗️ Clean Architecture** - Layered design with separation of concerns (API → Service → Repository)
- **📚 Auto-Generated Docs** - Interactive Swagger UI and ReDoc documentation
- **⚡ Async Operations** - Non-blocking I/O for high performance
- **🔒 Security First** - Input validation, error handling, and secure password storage

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (or local MongoDB instance)
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/e-commerce-backend.git
   cd e-commerce-backend
   ```

2. **Create virtual environment**

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
   ```

5. **Generate Prisma client**

   ```bash
   python -m prisma generate
   ```

6. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000`

- **📖 API Documentation**: http://localhost:8000/docs
- **📄 Alternative Docs**: http://localhost:8000/redoc
- **💚 Health Check**: http://localhost:8000/health

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
src/
├── api/                    # API Layer (Routes & Endpoints)
│   ├── deps.py            # Dependency injection
│   └── v1/                # API version 1
│       ├── auth.py        # Authentication endpoints
│       ├── products.py    # Product endpoints
│       ├── cart.py        # Cart endpoints
│       └── orders.py      # Order endpoints
├── core/                   # Core Layer (Configuration & Infrastructure)
│   ├── config.py          # Application settings
│   ├── security.py        # Security utilities (JWT, bcrypt)
│   └── database.py        # Database connection
├── schemas/                # Schema Layer (Data Validation)
│   ├── user.py            # User schemas
│   ├── product.py         # Product schemas
│   ├── cart.py            # Cart schemas
│   ├── order.py           # Order schemas
│   └── token.py           # Token schemas
├── services/               # Service Layer (Business Logic)
│   ├── auth_service.py    # Authentication logic
│   ├── product_service.py # Product business logic
│   ├── cart_service.py    # Cart business logic
│   └── order_service.py   # Order business logic
├── repositories/           # Repository Layer (Data Access)
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── cart_repository.py
│   └── order_repository.py
├── middlewares/            # Middleware Layer
│   └── error_handler.py   # Global error handling
├── utils/                  # Utilities
│   └── pagination.py      # Pagination helpers
└── main.py                # Application entry point
```

### Architecture Benefits

- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to add new features or modify existing ones
- **Flexibility**: Can swap implementations (e.g., change database) without affecting business logic

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint                | Description       | Auth Required |
| ------ | ----------------------- | ----------------- | ------------- |
| POST   | `/api/v1/auth/register` | Register new user | ❌            |
| POST   | `/api/v1/auth/login`    | Login user        | ❌            |

**Example: Register User**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure123"
  }'
```

**Response:**

```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### 📦 Products

| Method | Endpoint                | Description                        | Auth Required |
| ------ | ----------------------- | ---------------------------------- | ------------- |
| GET    | `/api/v1/products`      | Get all products (with pagination) | ❌            |
| GET    | `/api/v1/products/{id}` | Get single product                 | ❌            |
| POST   | `/api/v1/products`      | Create product                     | ✅            |
| PUT    | `/api/v1/products/{id}` | Update product                     | ✅            |
| DELETE | `/api/v1/products/{id}` | Delete product                     | ✅            |

**Query Parameters for GET /products:**

- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)
- `search` - Search by title or description
- `category` - Filter by category
- `sort` - Sort by price (`price_asc` or `price_desc`)

**Example: Get Products**

```bash
curl "http://localhost:8000/api/v1/products?page=1&page_size=10&category=Electronics&sort=price_asc"
```

**Example: Create Product**

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro",
    "description": "Latest Apple smartphone",
    "price": 999.99,
    "category": "Electronics",
    "imageUrl": "https://example.com/iphone.jpg"
  }'
```

### 🛒 Shopping Cart

| Method | Endpoint                  | Description               | Auth Required |
| ------ | ------------------------- | ------------------------- | ------------- |
| GET    | `/api/v1/cart`            | Get user cart             | ✅            |
| POST   | `/api/v1/cart/items`      | Add item to cart          | ✅            |
| PUT    | `/api/v1/cart/items/{id}` | Update cart item quantity | ✅            |
| DELETE | `/api/v1/cart/items/{id}` | Remove item from cart     | ✅            |

**Example: Add to Cart**

```bash
curl -X POST "http://localhost:8000/api/v1/cart/items" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "productId": "507f1f77bcf86cd799439011",
    "quantity": 2
  }'
```

### 📋 Orders

| Method | Endpoint              | Description            | Auth Required |
| ------ | --------------------- | ---------------------- | ------------- |
| GET    | `/api/v1/orders`      | Get order history      | ✅            |
| GET    | `/api/v1/orders/{id}` | Get specific order     | ✅            |
| POST   | `/api/v1/orders`      | Create order from cart | ✅            |

**Example: Create Order**

```bash
curl -X POST "http://localhost:8000/api/v1/orders" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🗄️ Database Schema

### User

```prisma
model User {
  id              String   @id @default(auto()) @map("_id") @db.ObjectId
  email           String   @unique
  hashedPassword  String
  createdAt       DateTime @default(now())
  cart            Cart?
  orders          Order[]
}
```

### Product

```prisma
model Product {
  id          String   @id @default(auto()) @map("_id") @db.ObjectId
  title       String
  description String
  price       Float
  category    String
  imageUrl    String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  cartItems   CartItem[]
  orderItems  OrderItem[]
}
```

### Cart & CartItem

```prisma
model Cart {
  id        String   @id @default(auto()) @map("_id") @db.ObjectId
  userId    String   @unique @db.ObjectId
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  user      User     @relation(fields: [userId], references: [id])
  items     CartItem[]
}

model CartItem {
  id        String  @id @default(auto()) @map("_id") @db.ObjectId
  cartId    String  @db.ObjectId
  productId String  @db.ObjectId
  quantity  Int
  cart      Cart    @relation(fields: [cartId], references: [id])
  product   Product @relation(fields: [productId], references: [id])
  @@unique([cartId, productId])
}
```

### Order & OrderItem

```prisma
model Order {
  id         String   @id @default(auto()) @map("_id") @db.ObjectId
  userId     String   @db.ObjectId
  totalPrice Float
  status     String   @default("pending")
  createdAt  DateTime @default(now())
  user       User     @relation(fields: [userId], references: [id])
  items      OrderItem[]
}

model OrderItem {
  id           String  @id @default(auto()) @map("_id") @db.ObjectId
  orderId      String  @db.ObjectId
  productId    String  @db.ObjectId
  productTitle String  # Snapshot for historical data
  productPrice Float   # Snapshot for historical data
  quantity     Int
  order        Order   @relation(fields: [orderId], references: [id])
  product      Product @relation(fields: [productId], references: [id])
}
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_auth.py -v
```

**Quick API Test:**

```bash
python quick_test.py
```

**Complete Test Suite:**

```bash
python complete_api_test.py
```

## 🔒 Security Features

- ✅ **Password Hashing** - bcrypt with salt
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Input Validation** - Pydantic schemas
- ✅ **CORS Configuration** - Configurable origins
- ✅ **Error Handling** - Consistent error responses
- ✅ **Environment Variables** - Sensitive data protection

## 🚀 Deployment

### Docker Deployment

The project includes a complete Docker setup, which allows you to run both the API and a local MongoDB instance seamlessly using Docker Compose.

1. **Verify Prerequisites**
   Ensure you have Docker and Docker Compose installed on your system.

2. **Run the application**
   ```bash
   docker-compose up --build
   ```
   This command will automatically:
   - Build the FastAPI backend image.
   - Start a local MongoDB instance.
   - Start the application on port `8000`.

3. **Stop the application**
   ```bash
   docker-compose down
   ```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Set up MongoDB Atlas with security
- [ ] Enable HTTPS
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up backup strategy

## 📈 Performance Optimization

### Current Optimizations

- Async/await for non-blocking I/O
- Database connection pooling (Prisma)
- Pagination for large datasets
- Indexed database fields

### Future Improvements

- Redis caching for frequently accessed data
- CDN for static assets
- Database query optimization
- Load balancing for horizontal scaling

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aryan Kumar**

- GitHub: [@aryacreations](https://github.com/aryacreations)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Prisma](https://www.prisma.io/) - Next-generation ORM
- [MongoDB](https://www.mongodb.com/) - NoSQL database
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

## 📞 Support

For questions or support, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**
