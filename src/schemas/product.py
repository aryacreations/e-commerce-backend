from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., gt=0)
    category: str
    imageUrl: str


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    imageUrl: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    title: str
    description: str
    price: float
    category: str
    imageUrl: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True
