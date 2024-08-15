from sqlalchemy import (String, Column, func,  Boolean, Text, Enum,
        JSON, ForeignKey, case)
from datetime import datetime, timezone
from enum import Enum as _Enum
from message_app.models import BaseModel, User
from sqlalchemy.ext.mutable import MutableDict, MutableList


class Notification(BaseModel):
    __tablename__ = "notificatins"

   to_user_id: Mapped[str] = mapped_column(String(60), nullable=False)
   url: Mapped[str] = mapped_column(String(60), nullable=False)
   content: Mapped[str] = mapped_column(Text, nullable=True)
   is_clicked: Mapped[bool] = mapped_column(Boolean, default=False)
   notification_type: Mapped[str] = mapped_column(String(60), nullable=False)

