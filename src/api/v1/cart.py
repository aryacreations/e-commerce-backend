from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse
from src.schemas.product import ProductResponse
from src.services import cart_service
from src.api.deps import get_current_user
from prisma.models import User

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user)
):
    """Add item to cart (protected endpoint)."""
    try:
        cart_item = await cart_service.add_to_cart(
            user_id=current_user.id,
            product_id=item_data.productId,
            quantity=item_data.quantity
        )
        
        return CartItemResponse(
            id=cart_item.id,
            productId=cart_item.productId,
            quantity=cart_item.quantity,
            product=ProductResponse(
                id=cart_item.product.id,
                title=cart_item.product.title,
                description=cart_item.product.description,
                price=cart_item.product.price,
                category=cart_item.product.category,
                imageUrl=cart_item.product.imageUrl,
                createdAt=cart_item.product.createdAt,
                updatedAt=cart_item.product.updatedAt
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding item to cart"
        )


@router.get("", response_model=CartResponse)
async def get_cart(current_user: User = Depends(get_current_user)):
    """Get user's cart (protected endpoint)."""
    try:
        result = await cart_service.get_user_cart(current_user.id)
        cart = result["cart"]
        total_price = result["total_price"]
        
        items = []
        if cart.items:
            for item in cart.items:
                items.append(CartItemResponse(
                    id=item.id,
                    productId=item.productId,
                    quantity=item.quantity,
                    product=ProductResponse(
                        id=item.product.id,
                        title=item.product.title,
                        description=item.product.description,
                        price=item.product.price,
                        category=item.product.category,
                        imageUrl=item.product.imageUrl,
                        createdAt=item.product.createdAt,
                        updatedAt=item.product.updatedAt
                    )
                ))
        
        return CartResponse(
            id=cart.id,
            userId=cart.userId,
            items=items,
            totalPrice=total_price,
            createdAt=cart.createdAt,
            updatedAt=cart.updatedAt
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching cart"
        )


@router.put("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: str,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update cart item quantity (protected endpoint)."""
    try:
        cart_item = await cart_service.update_cart_item(
            user_id=current_user.id,
            cart_item_id=item_id,
            quantity=item_data.quantity
        )
        
        return CartItemResponse(
            id=cart_item.id,
            productId=cart_item.productId,
            quantity=cart_item.quantity,
            product=ProductResponse(
                id=cart_item.product.id,
                title=cart_item.product.title,
                description=cart_item.product.description,
                price=cart_item.product.price,
                category=cart_item.product.category,
                imageUrl=cart_item.product.imageUrl,
                createdAt=cart_item.product.createdAt,
                updatedAt=cart_item.product.updatedAt
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating cart item"
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    item_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove item from cart (protected endpoint)."""
    try:
        await cart_service.remove_from_cart(
            user_id=current_user.id,
            cart_item_id=item_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing item from cart"
        )
