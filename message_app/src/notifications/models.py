from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from message_app.models import BaseModel


class Notification(BaseModel):
    __tablename__ = "notificatins"

    to_user_id: Mapped[str] = mapped_column(String(60), nullable=False)
    url: Mapped[str] = mapped_column(String(60), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_clicked: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_type: Mapped[str] = mapped_column(String(60), nullable=False)

