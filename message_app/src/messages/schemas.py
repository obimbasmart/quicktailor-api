from pydantic import BaseModel
from typing import List
from datetime import datetime
from message_app.models import UserType

class UserInfo(BaseModel):
    message_key: str
    user_type: UserType
    user_id: str 

class ProductItem(BaseModel):
    id: str
    name: str
    price: float
    image:str

class BaseMessage(BaseModel):
    id: str
    content: str  = None
    created_at: datetime

class MessageListResponse(BaseMessage):
    from_user_id: str
    to_user_id: str
class MessageHistoryResponse(BaseMessage):
    updated_at:datetime | None
    product: ProductItem |  None
    media: str = None
    from_user_id: str
    to_user_id: str

class SendMessageData(BaseModel):
    content: str =  None
    product: ProductItem = None
    media: str  = None
    message_key: str

class UpdateMessage(BaseModel):
    content:str 
    message_key:str
