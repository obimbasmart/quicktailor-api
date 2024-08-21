from pydantic import BaseModel
from typing import List
from datetime import datetime




class BaseNotification(BaseModel):
    content: str
    notification_type: str
    url: str
    reciever_id: str



class NotificationResponse(BaseNotification):
    id: str
    created_at:datetime
    is_clicked: bool
    to_user_id: str
