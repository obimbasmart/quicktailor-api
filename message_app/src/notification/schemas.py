from pydantic import BaseModel
from typing import List
from datetime import datetime
from message_app.models import UserType




class BaseNotification(BaseModel):
    content: str 
    notification_type: str
    url: str




class NotificationResponse(BaseNotification):
    id: str
    created_at:datetime
