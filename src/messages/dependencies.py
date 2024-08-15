from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.auth.dependencies import get_current_user
from src.tailors.CRUD import get_tailors
from src.tailors.dependencies import get_tailor_by_id, get_current_tailor
from dependencies import get_db
from typing import List
from pydantic import UUID4
from fastapi import HTTPException
from src.messages.schemas import MessageHistoryResponse, SendMessageData, UserInfo
import os
import requests


def send_user_info(req_body:UserInfo, db=Depends(get_db),
        current_user = Depends(get_current_user)):

    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    send_data = req_body.dict()
    send_data['user_type'] = send_data['user_type'].value
    response = requests.post("http://127.0.0.1:8001/chats", json=send_data, headers=headers)
    print("this is the response from the app", response.json())
    return response.json()

