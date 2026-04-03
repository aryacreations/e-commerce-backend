from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemResponse(BaseModel):
    id: str
    productId: str
    productTitle: str
    productPrice: float
    quantity: int
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: str
    userId: str
    totalPrice: float
    status: str
    items: List[OrderItemResponse]
    createdAt: datetime
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    pass
