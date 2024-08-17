import socketio
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.auth.config import settings as auth_settings
import jwt
from jwt.exceptions import InvalidTokenError
from socket_server import sio
from database import SessionLocal
from src.auth.utils import get_by_email
import os
from fastapi.encoders import jsonable_encoder
import requests
from src.messages.schemas import SendMessageData
from pydantic import ValidationError

db = SessionLocal()

# This dictionary will map user_ids to their corresponding socket session ids
connected_users = {}

# Function to manually validate the token and retrieve the user
def get_current_user(token: str, db: Session):
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

@sio.event
async def connect(sid, environ):
    # Extract the token from the query parameters
    query_string = environ.get('QUERY_STRING', '')
    token = None

    for param in query_string.split('&'):
        if param.startswith('token='):
            token = param.split('=')[1]
            break

    if not token:
        print("No token provided. Disconnecting.")
        await sio.disconnect(sid)
        return

    try:
        current_user = get_current_user(token, db)
        connected_users[current_user.id] = sid
        print(f"User {current_user.id} connected with session id {sid}")
    except HTTPException:
        print("Invalid token. Disconnecting.")
        await sio.disconnect(sid)

@sio.event
async def disconnect(sid):
    # Remove the user from connected_users when they disconnect
    user_id_to_remove = None
    for user_id, session_id in connected_users.items():
        if session_id == sid:
            user_id_to_remove = user_id
            break

    if user_id_to_remove:
        del connected_users[user_id_to_remove]
        print(f"User {user_id_to_remove} disconnected")

@sio.event
async def send_message(sid, data):
    # Get the sender_id from the data
    sender_id = data.get('sender_id')
    reciever_id = data.get('receiver_id')
    message_obj = data.get('message')
    if not reciever_id or not message_obj:
        await sio.emit("message_error", {"status": "error", "message": "Invalid reciever or message empty."}, room=sid)
        return
    # Verify that the sender_id matches the session ID in connected_users
    if connected_users.get(sender_id) != sid:
        await sio.emit("message_error", {"status": "error", "message": "Invalid sender."}, room=sid)
        return
    if not isinstance(message_obj, dict):
        await sio.emit("message_error", {"status": "error", "message": "Invalid message format. Expected an object."}, room=sid)
        return

    # Validate the message_obj against the SendMessageData model
    try:
        message_data = SendMessageData(**message_obj)
    except ValidationError as e:
        await sio.emit("message_error", {"status": "error", "message": "Invalid message format."}, room=sid)
        return

    send_data = jsonable_encoder(message_data)
    SECRET_KEY = os.getenv("SECRET_KEY")

    headers = {
        "x-secret-key": f"{SECRET_KEY}",
        "Content-Type": "application/json"
        }
    send_data = message_obj
    response = requests.post(f"http://127.0.0.1:8001/chats/{sender_id}/messages/{reciever_id}", json=send_data, headers=headers)
    
    if 'detail' in response.json() or 'errors' in response.json():
        await sio.emit("message_error", {"status": 'error', "message": (response.json()['detail'] 
             if 'detail' in response.json() else response.json()['errors'][0]['message'])}, room=sid)
        return
    # Send an acknowledgment to the sender
    else:
        await sio.emit("message_sent", {"status": "sent"}, room=sid)
        # Ensure the receiver is connected
        if reciever_id in connected_users:
            new_message = response.json()
            new_response = requests.patch(f"http://127.0.0.1:8001/chats/{new_message['to_user_id']}/messages/{new_message['id']}", headers=headers)
            reciever_sid = connected_users[reciever_id]
            data['message'] = new_response.json()
            await sio.emit("receive_message", data, room=reciever_sid)
            await sio.emit("message", {"status": "viewed", 'data':data}, room=sid)
            return
        #if the reciever is not online emit as not viewed
        else:
            data['message'] = response.json()
            await sio.emit("message", {"status": "not_viewed", 'data':data}, room=sid)

