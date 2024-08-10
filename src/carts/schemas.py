from pydantic import BaseModel, UUID4, computed_field, Field, EmailStr
from typing import List
from datetime import datetime


class AddCart(BaseModel):
    product_id: str
    measurements: dict

class RemoveCart(BaseModel):
    cart_id: str


class TailorInfo(BaseModel):
    id: UUID4
    brand_name: str | None
    photo: str | None
    is_available: bool

    class Config:
        from_attributes = True

class ProductInfo(BaseModel):
    id: UUID4
    name: str
    price: float
    images: list

class CartItems(BaseModel):
    id: str
    product: ProductInfo
    tailor: TailorInfo


