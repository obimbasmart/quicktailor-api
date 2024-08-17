import socketio

sio = socketio.AsyncServer(async_mode="asgi")

class MessageNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        # Add the connection logic specific to messages
        print(f"User connected to Message namespace: {sid}")

    def on_disconnect(self, sid):
        # Add the disconnection logic specific to messages
        print(f"User disconnected from Message namespace: {sid}")

    async def on_send_message(self, sid, data):
        # Implement the message sending logic here
        await send_message(sid, data)  # Reuse your existing logic if applicable

class NotificationNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        # Add the connection logic specific to notifications
        print(f"User connected to Notification namespace: {sid}")

    def on_disconnect(self, sid):
        # Add the disconnection logic specific to notifications
        print(f"User disconnected from Notification namespace: {sid}")

    # Implement any specific event handling for notifications

# Register the namespaces
sio.register_namespace(MessageNamespace('/messages'))
sio.register_namespace(NotificationNamespace('/notifications'))

