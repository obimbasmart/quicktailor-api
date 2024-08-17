from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from dependencies import get_db
from typing import List
from fastapi import HTTPException
from src.notifications.schemas import BaseNotification, NotificationResponse
import os
import requests

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)



@router.post('/{user_id}', response_model=NotificationResponse | dict)
def send_message(req_body:BaseNotification, user_id,  db=Depends(get_db),
        current_user = Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    response = requests.post(f"http://127.0.0.1:8001/notifications/{user_id}", json=req_body.dict(), headers=headers)
    return response.json()

@router.get('/{user_id}', response_model=List[NotificationResponse] | dict)
def get_messages(user_id: str,  db=Depends(get_db),
        current_user = Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    response = requests.get(f"http://127.0.0.1:8001/notifications/{user_id}",  headers=headers)
    return response.json()

