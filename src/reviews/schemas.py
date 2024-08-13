from pydantic import BaseModel
from typing import List


class UploadReview(BaseModel):
    text: str
    seller_communication_level: int  = None
    product_quality: int  = None
    product_as_described: int = None
    recommend_to_friend: int = None

