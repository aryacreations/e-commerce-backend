from typing import Optional
from prisma.models import User
from src.core.security import hash_password, verify_password, create_access_token
from src.repositories import user_repository
from src.schemas.user import UserCreate
import re


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    """Validate password strength (minimum 6 characters)."""
    return len(password) >= 6


async def register_user(user_data: UserCreate) -> User:
    """Register a new user."""
    # Validate email format
    if not validate_email(user_data.email):
        raise ValueError("Invalid email format")
    
    # Validate password strength
    if not validate_password(user_data.password):
        raise ValueError("Password must be at least 6 characters long")
    
    # Check for duplicate email
    existing_user = await user_repository.get_user_by_email(user_data.email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    user = await user_repository.create_user(user_data.email, hashed_password)
    
    return user


async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password."""
    user = await user_repository.get_user_by_email(email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashedPassword):
        return None
    
    return user


async def get_current_user(token: str) -> Optional[User]:
    """Get current user from JWT token."""
    from src.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if not payload:
        return None
    
    email = payload.get("sub")
    if not email:
        return None
    
    user = await user_repository.get_user_by_email(email)
    return user
