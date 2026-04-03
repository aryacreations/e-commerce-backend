# E-Commerce Application - Complete Setup Guide

## 🚀 Quick Start

### Option 1: Using the Start Script (Windows)

```bash
# Double-click start.bat or run:
start.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**

```bash
uvicorn src.main:app --reload
```

**Terminal 2 - Frontend:**

```bash
cd frontend
streamlit run app.py
```

## 📋 Prerequisites

- Python 3.9+
- MongoDB Atlas account (or local MongoDB)
- Git

## 🔧 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/aryacreations/e-commerce-backend.git
cd e-commerce-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
pip install -r requirements.txt
cd ..
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory:

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

### 6. Generate Prisma Client

```bash
prisma generate
```

### 7. Run the Application

```bash
# Backend
uvicorn src.main:app --reload

# Frontend (in another terminal)
cd frontend
streamlit run app.py
```

## 🌐 Access Points

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📱 Using the Application

### 1. Register an Account

- Open http://localhost:8501
- Use the sidebar to register
- Email: `test@example.com`
- Password: `password123` (min 6 characters)

### 2. Browse Products

- Go to the "Products" tab
- Search, filter by category, or sort by price
- Add products to cart

### 3. Manage Cart

- Go to the "Cart" tab
- Update quantities or remove items
- Click "Checkout" to place order

### 4. View Orders

- Go to the "Orders" tab
- See your order history and details

### 5. Add Products

- Go to the "Add Product" tab
- Fill in product details
- Submit to add new products

## 🧪 Testing

### Run Tests

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

## 📊 Database Schema

### Collections

**users**

- id (ObjectId)
- email (String, unique)
- hashedPassword (String)
- createdAt (DateTime)

**products**

- id (ObjectId)
- title (String)
- description (String)
- price (Float)
- category (String)
- imageUrl (String)
- createdAt, updatedAt (DateTime)

**carts**

- id (ObjectId)
- userId (ObjectId, unique)
- createdAt, updatedAt (DateTime)

**cart_items**

- id (ObjectId)
- cartId (ObjectId)
- productId (ObjectId)
- quantity (Integer)

**orders**

- id (ObjectId)
- userId (ObjectId)
- totalPrice (Float)
- status (String)
- createdAt (DateTime)

**order_items**

- id (ObjectId)
- orderId (ObjectId)
- productId (ObjectId)
- productTitle (String)
- productPrice (Float)
- quantity (Integer)

## 🔑 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Products

- `GET /api/v1/products` - Get all products (with pagination, search, filter, sort)
- `GET /api/v1/products/{id}` - Get single product
- `POST /api/v1/products` - Create product (protected)
- `PUT /api/v1/products/{id}` - Update product (protected)
- `DELETE /api/v1/products/{id}` - Delete product (protected)

### Cart

- `GET /api/v1/cart` - Get user cart (protected)
- `POST /api/v1/cart/items` - Add item to cart (protected)
- `PUT /api/v1/cart/items/{id}` - Update cart item (protected)
- `DELETE /api/v1/cart/items/{id}` - Remove from cart (protected)

### Orders

- `GET /api/v1/orders` - Get user orders (protected)
- `GET /api/v1/orders/{id}` - Get specific order (protected)
- `POST /api/v1/orders` - Create order from cart (protected)

## 🛠️ Troubleshooting

### Backend won't start

- Check if MongoDB connection string is correct
- Ensure Prisma client is generated: `prisma generate`
- Check if port 8000 is available

### Frontend won't start

- Ensure backend is running first
- Check if port 8501 is available
- Verify requests library is installed

### Database connection issues

- Verify MongoDB Atlas IP whitelist
- Check database URL format
- Ensure network connectivity

### Import errors

- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.9+)

## 📝 Development Tips

### Adding New Features

1. Update Prisma schema in `prisma/schema.prisma`
2. Run `prisma generate`
3. Create Pydantic schemas in `src/schemas/`
4. Implement repository in `src/repositories/`
5. Implement service in `src/services/`
6. Create API endpoints in `src/api/v1/`
7. Write tests in `tests/`

### Code Structure

- **API Layer**: Route handlers (FastAPI)
- **Service Layer**: Business logic
- **Repository Layer**: Database operations
- **Schema Layer**: Request/response validation (Pydantic)

## 🚢 Deployment

### Backend Deployment (Heroku Example)

```bash
# Create Procfile
echo "web: uvicorn src.main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
git push heroku main
```

### Frontend Deployment (Streamlit Cloud)

1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy frontend/app.py

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prisma Python Documentation](https://prisma-client-py.readthedocs.io/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## 📄 License

MIT License

## 👨‍💻 Author

Arya Creations

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Prisma for the modern ORM
- MongoDB for the flexible database
- Streamlit for rapid frontend development
