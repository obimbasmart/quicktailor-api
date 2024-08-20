from fastapi import APIRouter, Depends, HTTPException
from typing import List
from msg.dependencies import get_db
from msg.src.notifications.schemas import BaseNotification, NotificationResponse
from msg.src.notifications.CRUD import (
    create_new_notification, get_notifications)
from msg.src.messages.dependencies import verify_secret_key

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)


@router.post('/{user_id}', response_model=NotificationResponse, dependencies=[Depends(verify_secret_key)])
def save_notification(req_body: BaseNotification, user_id: str,  db=Depends(get_db)):
    new_notification = create_new_notification(req_body, user_id, db)
    return new_notification


@router.get('/{user_id}', response_model=List[NotificationResponse])
def get_user_notification(user_id: str, db=Depends(get_db)):
    user_notifications = get_notifications(user_id, db)
    return user_notifications
