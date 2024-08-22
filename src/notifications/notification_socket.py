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
from src.notifications.schemas import NotificationResponse
from pydantic import ValidationError

# Assuming these are available globally or imported
db = SessionLocal()  # Adjust if necessary
connected_users = {}
NOTIFICATION_KEY = os.getenv('NOTIFICATION_KEY')

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


class NotificationNamespace(socketio.AsyncNamespace):
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
            current_user = get_current_user(token, db)
            connected_users[current_user.id] = sid
            print(f"User {current_user.id} connected  to notificationwith session id {sid}")
        except HTTPException:
            if token == NOTIFICATION_KEY:
                connected_users['notification_app'] = sid
                print(f"Notification Application connected  to notification event with session id {sid}")
            else:
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

       
    async def on_send_notification(self, sid, data):
        print("we call notification here", connected_users) 
        if not data.get('secret_xxn_key'):
            await self.emit("message_error", {"status": "error", "message": "Unauthorized access."}, room=sid)
            return
        reciever_sid = connected_users[data.get('reciever_id')]
        
        """try:
            notification_data = NotificationResponse(**data.get('notification'))
        except ValidationError:
            await self.emit("message_error", {"status": "error", "message": "Invalid notification format."}, room=sid)
            return
        """
    
        await self.emit('notification', data.get('notification'), room=reciever_sid)
