from typing import Optional
from prisma.models import Cart, CartItem
from src.core.database import get_db


async def get_or_create_cart(user_id: str) -> Cart:
    """Get or create cart for user."""
    db = get_db()
    
    cart = await db.cart.find_unique(
        where={"userId": user_id},
        include={"items": {"include": {"product": True}}}
    )
    
    if not cart:
        cart = await db.cart.create(
            data={"userId": user_id},
            include={"items": {"include": {"product": True}}}
        )
    
    return cart


async def add_cart_item(cart_id: str, product_id: str, quantity: int) -> CartItem:
    """Add or update cart item."""
    db = get_db()
    
    # Check if item already exists
    existing_item = await db.cartitem.find_first(
        where={"cartId": cart_id, "productId": product_id}
    )
    
    if existing_item:
        # Update quantity
        cart_item = await db.cartitem.update(
            where={"id": existing_item.id},
            data={"quantity": existing_item.quantity + quantity},
            include={"product": True}
        )
    else:
        # Create new item
        cart_item = await db.cartitem.create(
            data={
                "cartId": cart_id,
                "productId": product_id,
                "quantity": quantity
            },
            include={"product": True}
        )
    
    return cart_item


async def get_cart_with_items(user_id: str) -> Optional[Cart]:
    """Get cart with all items and product details."""
    db = get_db()
    
    cart = await db.cart.find_unique(
        where={"userId": user_id},
        include={"items": {"include": {"product": True}}}
    )
    
    return cart


async def update_cart_item_quantity(cart_item_id: str, quantity: int) -> CartItem:
    """Update cart item quantity."""
    db = get_db()
    
    cart_item = await db.cartitem.update(
        where={"id": cart_item_id},
        data={"quantity": quantity},
        include={"product": True}
    )
    
    return cart_item


async def remove_cart_item(cart_item_id: str) -> bool:
    """Remove item from cart."""
    db = get_db()
    
    try:
        await db.cartitem.delete(where={"id": cart_item_id})
        return True
    except:
        return False


async def clear_cart(user_id: str) -> bool:
    """Clear all items from user's cart."""
    db = get_db()
    
    try:
        cart = await db.cart.find_unique(where={"userId": user_id})
        if cart:
            await db.cartitem.delete_many(where={"cartId": cart.id})
        return True
    except:
        return False


async def get_cart_item_by_id(cart_item_id: str) -> Optional[CartItem]:
    """Get cart item by ID."""
    db = get_db()
    
    cart_item = await db.cartitem.find_unique(
        where={"id": cart_item_id},
        include={"cart": True, "product": True}
    )
    
    return cart_item
