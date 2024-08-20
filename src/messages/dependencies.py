from fastapi import Depends
from src.auth.dependencies import get_current_user
from dependencies import get_db
from src.messages.schemas import UserMessageData
import os
import requests
from config import get_settings

settings = get_settings()

headers = {
    "x-secret-key": f"{settings.SECRET_KEY}",
    "Content-Type": "application/json"
}


def send_user_data_to_message_system(user_data: UserMessageData):
    data = user_data.model_dump()
    print(data)
    response = requests.post(
        "http://127.0.0.1:8001/chats", json=data, headers=headers)
    return response.json()


def get_user_msg_data(user):
    return UserMessageData(message_key=user.message_key,
                           user_id=user.id,
                           user_type=type(user).__name__.lower())