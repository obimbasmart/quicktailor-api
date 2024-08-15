from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.tailors.CRUD import get_tailors
from src.tailors.dependencies import get_tailor_by_id, get_current_tailor
from dependencies import get_db
from typing import List
from pydantic import UUID4
from fastapi import HTTPException
from src.messages.schemas import (MessageHistoryResponse, SendMessageData, 
        UserInfo, MessageListResponse,  UpdateMessage)
import os 
import requests

router = APIRouter(
    prefix="/chats",
    tags=["chat"],
)



@router.post('/{from_user_id}/messages/{to_user_id}', response_model=MessageHistoryResponse | dict)
def send_message(req_body:SendMessageData, from_user_id:str, to_user_id: str,  db=Depends(get_db),
        current_user = Depends(get_current_user)):
    
    if from_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")
    
    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    send_data = {k: v for k, v in req_body if v is not None}
    if req_body.product:
        send_data['product'] = send_data['product'].dict()
    response = requests.post(f"http://127.0.0.1:8001/chats/{from_user_id}/messages/{to_user_id}", json=send_data, headers=headers)
    return response.json()

@router.get('/{from_user_id}/messages/{to_user_id}', response_model=List[MessageHistoryResponse] | dict)
def get_messages(from_user_id:str, to_user_id: str,  db=Depends(get_db),
        current_user = Depends(get_current_user)):

    if from_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    response = requests.get(f"http://127.0.0.1:8001/chats/{from_user_id}/messages/{to_user_id}",  headers=headers)
    return response.json()

@router.put('/{from_user_id}/messages/{message_id}', response_model=MessageHistoryResponse | dict)
def update_message(req_body:UpdateMessage, from_user_id:str, message_id:str,  db=Depends(get_db),
        current_user = Depends(get_current_user)):

    if from_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    response = requests.put(f"http://127.0.0.1:8001/chats/{from_user_id}/messages/{message_id}", json=req_body.dict(), headers=headers)
    return response.json()


@router.get('/{user_id}/messages', response_model=List[MessageListResponse] | dict)
def get_messages(user_id: str,  db=Depends(get_db),
        current_user = Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Couldn't validate credentials")

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    response = requests.get(f"http://127.0.0.1:8001/chats/{user_id}/messages",  headers=headers)
    return response.json()


