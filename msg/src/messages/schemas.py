from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional
from datetime import datetime
from msg.models import UserType


class UserInfo(BaseModel):
    message_key: str
    user_type: UserType
    user_id: str


class ProductItem(BaseModel):
    id: str
    name: str
    price: float
    image: str


class BaseMessage(BaseModel):
    id: str
    content: str | None
    created_at: datetime
    is_viewed: bool


class MessageListResponse(BaseMessage):
    from_user_id: str
    to_user_id: str


class MessageHistoryResponse(BaseMessage):
    updated_at: datetime | None
    product: ProductItem | None
    media: str = None
    from_user_id: str
    to_user_id: str


class ProductItem(BaseModel):
    # Define the ProductItem model according to your needs
    pass


class SendMessageData(BaseModel):
    content: Optional[str] = None
    product: Optional[ProductItem] = None
    media: Optional[str] = None
    message_key: str

    @model_validator(mode='after')
    def check_constraints(self):
        # Ensure at least one of content, product, or media is not None
        if not any([self.content, self.product, self.media]):
            raise ValueError(
                "At least one of 'content', 'product', or 'media' must be provided.")

        # If 'product' is provided, 'content' or 'media' must not be None
        if self.product and not any([self.content, self.media]):
            raise ValueError(
                "'content' or 'media' must be provided if 'product' is specified.")

        return self


class UpdateMessage(BaseModel):
    content: str
    message_key: str


class BaseResponse(BaseModel):
    message: str
