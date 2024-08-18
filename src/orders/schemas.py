from pydantic import BaseModel, UUID4, computed_field, Field, EmailStr
from typing import List, Dict
from datetime import datetime, timedelta
from src.orders.models import OrderStatus
from src.products.schemas import TailorListInfo
from src.orders.constants import OrderStageStatus


class ProductInfo(BaseModel):
    id: UUID4
    name: str
    price: float
    images: List = Field(exclude=True, default=[])
    image_cover_index: int = Field(exclude=True, default=0)

    @computed_field
    @property
    def image(self) -> str:
        return self.images[self.image_cover_index | 0]

    class Config:
        from_attributes = True


class TailorInfo(BaseModel):
    id: str
    brand_name: str | None
    photo: str | None
    is_available: bool


class OrderListItem(BaseModel):
    id: str
    created_at: datetime
    status: str
    amount_paid: float
    product: ProductInfo
    tailor: TailorInfo | None

    class Config:
        from_attributes = True


class UserInfo(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class TailorOrderListItem(BaseModel):
    id: str
    created_at: datetime
    status: str
    product: ProductInfo
    user: UserInfo

    class Config:
        from_attributes = True


class CreateOrder(BaseModel):
    reference: str
    user_id: str

    class Config:
        extra = 'forbid'


class ProductItem(BaseModel):
    name: str
    estimated_tc: int = Field(exclude=True)
    images: List = Field(exclude=True)
    image_cover_index: int = Field(exclude=True)


    @computed_field
    @property
    def image(self) -> str:
        return self.images[self.image_cover_index]



class PaymentItem(BaseModel):
    created_at: datetime
    amount_paid: float


class UserItem(BaseModel):
    username: str
    email: EmailStr
    phone_no: str = None


class OrderStage(BaseModel):
    id: int
    title: str
    status: OrderStageStatus
    updated_at: datetime | None = None

class UserOrderItem(BaseModel):
    id: str
    status: OrderStatus
    created_at: datetime
    product: ProductItem
    user: UserItem
    tailor: TailorListInfo
    stages: Dict[str, OrderStage]
    customization_code: str | None = None

    @computed_field
    @property
    def completion_date(self) -> datetime:
        return self.created_at + timedelta(self.product.estimated_tc)