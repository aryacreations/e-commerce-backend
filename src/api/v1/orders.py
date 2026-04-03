from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.schemas.order import OrderResponse, OrderItemResponse
from src.services import order_service
from src.api.deps import get_current_user
from prisma.models import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(current_user: User = Depends(get_current_user)):
    """Create order from cart (protected endpoint)."""
    try:
        order = await order_service.create_order(current_user.id)
        
        items = [
            OrderItemResponse(
                id=item.id,
                productId=item.productId,
                productTitle=item.productTitle,
                productPrice=item.productPrice,
                quantity=item.quantity
            ) for item in order.items
        ]
        
        return OrderResponse(
            id=order.id,
            userId=order.userId,
            totalPrice=order.totalPrice,
            status=order.status,
            items=items,
            createdAt=order.createdAt
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order"
        )


@router.get("", response_model=List[OrderResponse])
async def get_orders(current_user: User = Depends(get_current_user)):
    """Get user's order history (protected endpoint)."""
    try:
        orders = await order_service.get_user_orders(current_user.id)
        
        return [
            OrderResponse(
                id=order.id,
                userId=order.userId,
                totalPrice=order.totalPrice,
                status=order.status,
                items=[
                    OrderItemResponse(
                        id=item.id,
                        productId=item.productId,
                        productTitle=item.productTitle,
                        productPrice=item.productPrice,
                        quantity=item.quantity
                    ) for item in order.items
                ],
                createdAt=order.createdAt
            ) for order in orders
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching orders"
        )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific order (protected endpoint)."""
    try:
        order = await order_service.get_order_by_id(current_user.id, order_id)
        
        items = [
            OrderItemResponse(
                id=item.id,
                productId=item.productId,
                productTitle=item.productTitle,
                productPrice=item.productPrice,
                quantity=item.quantity
            ) for item in order.items
        ]
        
        return OrderResponse(
            id=order.id,
            userId=order.userId,
            totalPrice=order.totalPrice,
            status=order.status,
            items=items,
            createdAt=order.createdAt
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
            detail="Error fetching order"
        )
