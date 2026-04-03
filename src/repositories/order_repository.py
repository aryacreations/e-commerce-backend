from typing import List, Optional
from prisma.models import Order, OrderItem
from src.core.database import get_db


async def create_order(user_id: str, total_price: float, order_items: List[dict]) -> Order:
    """Create a new order with order items."""
    db = get_db()
    
    order = await db.order.create(
        data={
            "userId": user_id,
            "totalPrice": total_price,
            "status": "pending",
            "items": {
                "create": order_items
            }
        },
        include={"items": {"include": {"product": True}}}
    )
    
    return order


async def get_user_orders(user_id: str) -> List[Order]:
    """Get all orders for a user."""
    db = get_db()
    
    orders = await db.order.find_many(
        where={"userId": user_id},
        include={"items": {"include": {"product": True}}},
        order={"createdAt": "desc"}
    )
    
    return orders


async def get_order_by_id(order_id: str) -> Optional[Order]:
    """Get order by ID with items."""
    db = get_db()
    
    order = await db.order.find_unique(
        where={"id": order_id},
        include={"items": {"include": {"product": True}}}
    )
    
    return order
