import socketio
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.auth.config import settings as auth_settings
import jwt
from jwt.exceptions import InvalidTokenError
from database import SessionLocal
from src.auth.utils import get_by_email
import os
from fastapi.encoders import jsonable_encoder
import requests
from src.messages.schemas import SendMessageData
from pydantic import ValidationError

db = SessionLocal()  
connected_users = {}

SECRET_KEY = os.getenv("SECRET_KEY")
headers = { 
            "x-secret-key": f"{SECRET_KEY}",
            "Content-Type": "application/json"
          }
 

# Function to manually validate the token and retrieve the user
def get_current_user_for_socket(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    # Your user retrieval function
    user = get_by_email(email, db)
    if user is None:
        raise credentials_exception
    return user

async def validate_input_data(self, sid, sender_id, reciever_id, message_obj):
    if not reciever_id or not message_obj:
        await self.emit("message_error", {"status": "error", "message": "Invalid sender, receiver, or message."}, room=sid)
        return False
    if connected_users.get(sender_id) != sid:
        await self.emit("message_error", {"status": "error", "message": "Invalid sender."}, room=sid)
        return False
    if not isinstance(message_obj, dict):
        await self.emit("message_error", {"status": "error", "message": "Invalid message format. Expected an object."}, room=sid)
        return False
    return True

class MessageNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        # Extract the token from the query parameters
        query_string = environ.get('QUERY_STRING', '')
        token = None
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break
        if not token:
            print("No token provided. Disconnecting.")
            await self.disconnect(sid)
            return
        try:
            current_user = get_current_user_for_socket(token, db)
            connected_users[current_user.id] = sid
            print(f"User {current_user.id} connected with session id {sid}")
        except HTTPException:
            print("Invalid token. Disconnecting.")
            await self.disconnect(sid)

    async def on_disconnect(self, sid):
        # Remove the user from connected_users when they disconnect
        user_id_to_remove = None
        for user_id, session_id in connected_users.items():
            if session_id == sid:
                user_id_to_remove = user_id
                break
        if user_id_to_remove:
            del connected_users[user_id_to_remove]
            print(f"User {user_id_to_remove} disconnected")
    
    async def on_send_message(self, sid, data):
        sender_id = data.get('sender_id')
        message_obj = data.get('message')
        reciever_id = data.get("reciever_id")
        validate_data = await validate_input_data( self, sid, sender_id, reciever_id, message_obj)
        if not validate_data:
            return
        try:
            message_data = SendMessageData(**data.get('message'))
        except ValidationError:
            await self.emit("message_error", {"status": "error", "message": "Invalid message format."}, room=sid)
            return
        
        send_msg_data = jsonable_encoder(message_data)
        message_response = requests.post(f"http://127.0.0.1:8001/chats/{sender_id}/messages/{reciever_id}", json=send_msg_data, headers=headers)
        
        if 'detail' in message_response.json() or 'errors' in message_response.json():
            await self.emit("message_error", {"status": 'error', "message": message_response.json().get('detail', 'An error occurred.')}, room=sid)
            return
        else:
            await self.emit("message_sent", {"status": "sent"}, room=sid)
            from src.notifications.notification_socket import connected_users as notification_connected_users, NOTIFICATION_KEY
            from src.messages.message_list_socket import connected_users as msg_list_connected_users, MESSAGE_LIST_KEY
            from socket_server import connect_and_rearrange_message_list, connect_and_send_notification
            response = requests.get(f"http://127.0.0.1:8001/chats/{reciever_id}/messages", headers=headers)
            if reciever_id in msg_list_connected_users:
                await connect_and_rearrange_message_list(MESSAGE_LIST_KEY, response.json(), reciever_id)
                await self.emit("message", {"status": "not_viewed", 'data': message_response.json()}, room=sid)
            elif reciever_id in connected_users:
                reciever_sid = connected_users[reciever_id]
                msg_viewed_response = requests.patch(f"http://127.0.0.1:8001/chats/{reciever_id}/messages/{message_response.json()['id']}", headers=headers)
                await self.emit("recieve_message", msg_viewed_response.json(), room=reciever_sid)
                await self.emit("message_view", {"status": "viewed", 'data': msg_viewed_response.json()}, room=sid)
            else:
                notification_data = {"content": "You have a new message", "notification_type": "message",
                        "url":f"/chats/{reciever_id}/messages/{sender_id}", "reciever_id": reciever_id}
                res = requests.post(f"http://127.0.0.1:8001/notifications/{reciever_id}", json=notification_data, headers=headers)
                if reciever_id in notification_connected_users:
                    await connect_and_send_notification(NOTIFICATION_KEY, res.json(), reciever_id)
                await self.emit("message_view", {"status": "not_viewed", 'data': message_response.json()}, room=sid)

