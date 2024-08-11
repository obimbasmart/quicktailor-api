from pydantic import BaseModel, UUID4, computed_field, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from src.orders.models import OrderStatus
from src.products.schemas import TailorListInfo

class OrderItem(BaseModel):
    product_id: str
    measurements: dict
    customization_id: str = None

class ProductItem(BaseModel):
    name: str
    image: str


class PaymentItem(BaseModel):
    created_at: datetime
    amount_paid: float

class UserItem(BaseModel):
    username: str
    email: EmailStr
    phone_no: str = None

class UserOrderItem(BaseModel):
    id: str
    status: OrderStatus
    product: ProductItem
    user: UserItem
    tailor: TailorListInfo
    stages: list
    created_at: datetime
    customization_code: str = None
    completion_date: datetime | None
