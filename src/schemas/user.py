from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        """Truncate password to bcrypt's 72 byte limit if necessary"""
        while len(v.encode('utf-8')) > 72:
            v = v[:-1]
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    createdAt: datetime
    
    class Config:
        from_attributes = True
