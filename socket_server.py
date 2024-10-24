import socketio, asyncio
from src.messages.message_socket import MessageNamespace
from src.messages.message_list_socket import MessageListNamespace, connected_users as  msg_list_connected_users
from src.notifications.notification_socket import NotificationNamespace, connected_users
import os

notification_socket = socketio.AsyncClient()
message_list_socket = socketio.AsyncClient()

# Event handler for connection to the /notifications namespace
@notification_socket.event(namespace='/notifications')
async def connect():
    print("Connected to /notifications namespace")

@notification_socket.event(namespace='/notifications')
async def disconnect():
    print("Disconnected from /notifications namespace")

async def connect_and_send_notification(token, notification_data, reciever_id):
    if 'notification_app' not in connected_users:
        print("This is the connected_users in notification:  ", connected_users)
        try:
            await notification_socket.connect(
                f'http://localhost:8000/notifications?token={token}',
                transports=['websocket']
            )
        except socketio.exceptions.ConnectionError as e:
            print("Connections are  failed:", str(e))
    await notification_socket.emit('send_notification', {
            'secret_xxn_key': token,
            'notification': notification_data,
            'reciever_id': reciever_id
        }, namespace='/notifications')


#connection for rearranging message list
@message_list_socket.event(namespace='/message_lists')
async def connect():
    print("Connected to /message_list namespace")

@message_list_socket.event(namespace='/message_lists')
async def disconnect():
    print("Disconnected from /messages_lists namespace")

async def connect_and_rearrange_message_list(token, msg_list_data, reciever_id):
    if 'message_list_app' not in msg_list_connected_users:
        try:
            await message_list_socket.connect(
                f'http://localhost:8000/message_lists?token={token}',
                transports=['websocket']
            )
        except socketio.exceptions.ConnectionError as e:
            print("Connection failed:", str(e))
    await message_list_socket.emit('rearrange_message_list', {
            'secret_xxn_key': token,
            'message_list': msg_list_data,
            'reciever_id': reciever_id
        }, namespace='/message_lists')

#Registration of namespaces
sio = socketio.AsyncServer(async_mode="asgi")
sio.register_namespace(MessageNamespace('/messages'))
sio.register_namespace(NotificationNamespace('/notifications'))
sio.register_namespace(MessageListNamespace('/message_lists'))


