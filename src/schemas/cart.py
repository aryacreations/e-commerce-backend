from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from src.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    productId: str
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: str
    productId: str
    quantity: int
    product: ProductResponse
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: str
    userId: str
    items: List[CartItemResponse]
    totalPrice: float
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
