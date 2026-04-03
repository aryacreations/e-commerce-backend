from typing import Optional
from prisma.models import User
from src.core.database import get_db


async def create_user(email: str, hashed_password: str) -> User:
    """Create a new user."""
    db = get_db()
    try:
        user = await db.user.create(
            data={
                "email": email,
                "hashedPassword": hashed_password
            }
        )
        return user
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")


async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    db = get_db()
    try:
        user = await db.user.find_unique(where={"email": email})
        return user
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")


async def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    db = get_db()
    try:
        user = await db.user.find_unique(where={"id": user_id})
        return user
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")
