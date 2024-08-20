from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from msg.src.messages.dependencies import verify_by_id, get_user_by_id
from msg.src.notifications.schemas import BaseNotification
from msg.src.notifications.models import Notification


def create_new_notification(notification_data: BaseNotification, user_id: str, db: Session):

    user = verify_by_id(user_id, db)

    new_notification = Notification(
        **notification_data.model_dump(), to_user_id=user_id)

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def get_notifications(user_id: str, db: Session):

    verify_by_id(user_id, db)

    user_notifications = db.query(Notification).filter(
        Notification.to_user_id == user_id).all()

    return user_notifications
