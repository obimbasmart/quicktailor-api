from pydantic import BaseModel, UUID4, computed_field, Field, EmailStr
from typing import List, Dict
from datetime import datetime
from src.users.schemas import MeasurementItem


class AddToCart(BaseModel):
    product_id: str
    measurements: MeasurementItem

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
    images: list = Field(exclude=True)
    image_cover_index: int = Field(exclude=True)
    tailor: TailorInfo = Field(exclude=True)

    @computed_field
    @property
    def image(self) -> str:
        return self.images[self.image_cover_index]



class CartItem(BaseModel):
    id: str
    product: ProductInfo
    
    
    @computed_field
    @property
    def tailor(self) -> Dict:
        return self.product

