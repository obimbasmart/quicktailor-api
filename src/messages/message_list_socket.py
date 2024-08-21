import socketio
from fastapi import HTTPException, status
import os
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from src.messages.message_socket import db, get_current_user
# Assuming these are available globally or imported

connected_users = {}
MESSAGE_LIST_KEY = os.getenv('MESSAGE_LIST_KEY')


class MessageListNamespace(socketio.AsyncNamespace):
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
            print(f"User {current_user.id} connected to  Message_list_app with session id {sid}")
        except HTTPException:
            if token == MESSAGE_LIST_KEY:
                connected_users['message_list_app'] = sid

                print(f"Message_list Application connected  to Message_list event with session id {sid}")
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

       
    async def on_rearrange_message_list(self, sid, data):
        print("dslfjlkjd sdkljfsdljf ", connected_users) 
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
    
        await self.emit('rearrange_message_list', data.get('message_list'), room=reciever_sid)

