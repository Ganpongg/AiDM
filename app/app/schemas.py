from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import OrderStatus

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: int
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: Optional[str] = None
    sku: str

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: Optional[str]
    sku: str
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    shipping_address: str
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    shipping_address: str
    created_at: datetime
    items: List[OrderItemOut]
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
