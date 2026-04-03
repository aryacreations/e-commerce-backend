from typing import List
from prisma.models import Order
from src.repositories import order_repository, cart_repository


async def create_order(user_id: str) -> Order:
    """Create order from user's cart."""
    # Get user's cart
    cart = await cart_repository.get_cart_with_items(user_id)
    
    if not cart or not cart.items or len(cart.items) == 0:
        raise ValueError("Cannot create order from empty cart")
    
    # Calculate total price and prepare order items
    total_price = 0.0
    order_items = []
    
    for item in cart.items:
        item_total = item.product.price * item.quantity
        total_price += item_total
        
        # Create order item with product snapshot
        order_items.append({
            "productId": item.productId,
            "productTitle": item.product.title,
            "productPrice": item.product.price,
            "quantity": item.quantity
        })
    
    # Create order
    order = await order_repository.create_order(user_id, total_price, order_items)
    
    # Clear cart after successful order creation
    await cart_repository.clear_cart(user_id)
    
    return order


async def get_user_orders(user_id: str) -> List[Order]:
    """Get all orders for a user."""
    orders = await order_repository.get_user_orders(user_id)
    return orders


async def get_order_by_id(user_id: str, order_id: str) -> Order:
    """Get order by ID with ownership validation."""
    order = await order_repository.get_order_by_id(order_id)
    
    if not order:
        raise ValueError("Order not found")
    
    # Validate ownership
    if order.userId != user_id:
        raise PermissionError("Unauthorized access to order")
    
    return order
