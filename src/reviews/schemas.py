from pydantic import BaseModel, Field, computed_field
from typing import Dict
from uuid import UUID
from src.users.models import User
from src.orders.models import Order
from datetime import datetime
from src.reviews.models import Rating


class ProductReviewItem(BaseModel):
    id: UUID
    name: str
    price: float

class UploadReview(BaseModel):
    text: str
    product_quality: Rating
    seller_communication_level: int | None = None
    product_as_described: int | None = None
    recommend_to_friend: int | None = None


class ReviewItem(BaseModel):
    id: UUID
    text: str
    seller_communication_level: int | None = None
    product_quality: int  = None
    product_as_described: int = None
    recommend_to_friend: int = None
    
    user: object = Field(exclude=True)
    order: object = Field(exclude=True)
    created_at: datetime

    @computed_field
    @property
    def username(self) -> str:
        return self.user.username
    
    @computed_field
    @property
    def product(self) -> Dict:
        return ProductReviewItem.model_validate().model_dump()
    


