from fastapi import APIRouter, Depends, HTTPException
from typing import List
from message_app.dependencies import get_db
from message_app.src.messages.schemas import (MessageHistoryResponse, SendMessageData,
        UserInfo, UpdateMessage, MessageListResponse)
from message_app.src.messages.CRUD import (create_new_message, create_new_user,
        get_message_history, update_message, get_last_messages_list)
from message_app.src.messages.dependencies import verify_secret_key
router = APIRouter(
    prefix="/chats",
    tags=["chat"],
)



@router.post('/{from_user_id}/messages/{to_user_id}', response_model=MessageHistoryResponse, dependencies=[Depends(verify_secret_key)])
def send_message(req_body: SendMessageData, from_user_id: str, to_user_id: str, db=Depends(get_db)):
    new_msg = create_new_message(req_body, from_user_id, to_user_id, db)
    return new_msg

@router.post('', response_model=None, dependencies=[Depends(verify_secret_key)])
def save_user_info(req_body: UserInfo, db=Depends(get_db)):
    new_user = create_new_user(req_body, db)
    return {"success": "User created successfully", "user_id": new_user.id}


@router.get('/{from_user_id}/messages/{to_user_id}', response_model=List[MessageHistoryResponse], dependencies=[Depends(verify_secret_key)])
def send_message( from_user_id: str, to_user_id: str, db=Depends(get_db)):
    message_history = get_message_history(from_user_id, to_user_id, db)
    return message_history

@router.put('/{from_user_id}/messages/{message_id}', response_model=MessageHistoryResponse, dependencies=[Depends(verify_secret_key)])
def send_message(req_body:UpdateMessage, from_user_id:str,  message_id: str,  db=Depends(get_db)):
    updated_message = update_message(req_body, from_user_id, message_id, db)
    return updated_message


@router.get('/{user_id}/messages', response_model=List[MessageListResponse], dependencies=[Depends(verify_secret_key)])
def send_message(user_id:str, db = Depends(get_db)):
    
    message_list = get_last_messages_list(user_id, db)
    return message_list