from pydantic import BaseModel, Field, computed_field
from typing import Dict
from uuid import UUID4
from src.users.models import User
from src.orders.models import Order
from datetime import datetime

class ProductReviewItem(BaseModel):
    id: UUID4
    name: str
    price: float

class UploadReview(BaseModel):
    text: str
    seller_communication_level: int  = None
    product_quality: int  = None
    product_as_described: int = None
    recommend_to_friend: int = None


class ReviewItem(UploadReview):
    id: UUID4
    text: str
    seller_communication_level: int  = None
    product_quality: int  = None
    product_as_described: int = None
    recommend_to_friend: int = None
    
    user: User = Field(exclude=True)
    order: Order = Field(exclude=True)
    created_at: datetime

    @computed_field
    @property
    def username(self) -> str:
        return self.user.username
    
    @computed_field
    @property
    def product(self) -> Dict:
        return ProductReviewItem.model_validate().model_dump()
    


