from pydantic import BaseModel
from typing import List
from datetime import datetime




class BaseNotification(BaseModel):
    content: str 
    notification_type: str
    url: str



class NotificationResponse(BaseNotification):
    id: str
    created_at:datetime
    is_clicked: bool
