from typing import Dict
from prisma.models import CartItem
from src.repositories import cart_repository, product_repository


async def add_to_cart(user_id: str, product_id: str, quantity: int) -> CartItem:
    """Add item to cart with validation."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    
    # Validate product exists
    product = await product_repository.get_product_by_id(product_id)
    if not product:
        raise ValueError("Product not found")
    
    # Get or create cart
    cart = await cart_repository.get_or_create_cart(user_id)
    
    # Add item to cart
    cart_item = await cart_repository.add_cart_item(cart.id, product_id, quantity)
    
    return cart_item


async def remove_from_cart(user_id: str, cart_item_id: str) -> bool:
    """Remove item from cart with ownership validation."""
    # Get cart item
    cart_item = await cart_repository.get_cart_item_by_id(cart_item_id)
    
    if not cart_item:
        raise ValueError("Cart item not found")
    
    # Validate ownership
    if cart_item.cart.userId != user_id:
        raise PermissionError("Unauthorized access to cart item")
    
    # Remove item
    success = await cart_repository.remove_cart_item(cart_item_id)
    return success


async def update_cart_item(user_id: str, cart_item_id: str, quantity: int) -> CartItem:
    """Update cart item quantity with validation."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    
    # Get cart item
    cart_item = await cart_repository.get_cart_item_by_id(cart_item_id)
    
    if not cart_item:
        raise ValueError("Cart item not found")
    
    # Validate ownership
    if cart_item.cart.userId != user_id:
        raise PermissionError("Unauthorized access to cart item")
    
    # Update quantity
    updated_item = await cart_repository.update_cart_item_quantity(cart_item_id, quantity)
    
    return updated_item


async def get_user_cart(user_id: str) -> Dict:
    """Get user cart with total price calculation."""
    cart = await cart_repository.get_cart_with_items(user_id)
    
    if not cart:
        cart = await cart_repository.get_or_create_cart(user_id)
    
    # Calculate total price
    total_price = 0.0
    if cart.items:
        for item in cart.items:
            total_price += item.product.price * item.quantity
    
    return {
        "cart": cart,
        "total_price": total_price
    }


async def clear_cart(user_id: str) -> bool:
    """Clear user's cart."""
    success = await cart_repository.clear_cart(user_id)
    return success
