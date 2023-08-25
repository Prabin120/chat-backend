import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chat.models import ChatMessage
from apps.user.models import User
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

class ChatConsumer(AsyncWebsocketConsumer):
    online_users = {}
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user = await self.get_user(self.user_id)
        self.online_users[self.user_id] = self.channel_name  # Store user's WebSocket channel
        await self.accept()

    async def disconnect(self, close_code):
        del self.online_users[self.user_id]  # Remove user from online users

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'message':
            message = text_data_json['message']
            recipient_id = text_data_json['recipient_id']
            
            msg_obj = await self.save_message(message,recipient_id)
            recipient_channel_name = self.online_users.get(recipient_id)
            # Check if the recipient is online
            if recipient_channel_name:
                await msg_obj.mark_as_delivered()
                await self.send_message(action, message, recipient_channel_name,msg_obj.timestamp,msg_obj.message_id)
        elif action == 'delete_message':
            message_id = text_data_json['message_id']
            success = await self.delete_message(message_id)
            await self.send_response(action,message_id,success)
        elif action == 'like_message':
            message_id = text_data_json['message_id']
            like = text_data_json['like']
            success = await self.like_message(message_id,like)
            await self.send_response(action,message_id,success)
        # else:
            # Store the message in the database for offline user
            # await self.save_message_offline(recipient_id, action, message)

    async def send_message(self, action, message, recipient_channel_name,timestamp,message_id):
        channel_layer = get_channel_layer()

        await channel_layer.send(
            recipient_channel_name,
            {
                "type": "chat.message",
                "action": action,
                "message_id":message_id,
                "message": message,
                "timestamp":timestamp
            }
        )
    async def send_response(self, action,message_id,success):
        channel_layer = get_channel_layer()
        await channel_layer.send(
            self.channel_name,
            {
                "type": "chat.response",
                "action": action,
                "message_id":message_id,
                "success":success,
            }
        )

    async def chat_message(self, event):
        message_id = str(event['message_id'])
        message = event['message']
        timestamp = str(event['timestamp'])
        action = event['action']
        await self.send(text_data=json.dumps({
            'action': action,
            'message_id':message_id,
            'message': message,
            'timestamp':timestamp
        }))

    async def chat_response(self, event):
        message_id = str(event['message_id'])
        action = event['action']
        success = event['success']
        await self.send(text_data=json.dumps({
            'action': action,
            'message_id':message_id,
            'success': success
        }))

    
    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            obj = ChatMessage.objects.get(message_id=message_id)
            if obj.sender == self.user:
                obj.delete()
                return True
            else:
                return False
        except:
            return False
        
    @database_sync_to_async
    def like_message(self, message_id,like):
        try:
            obj = ChatMessage.objects.get(message_id=message_id)
            if obj.receiver == self.user:
                obj.like = like
                obj.save()
                return True
            else:
                return False
        except:
            return False

    @database_sync_to_async
    def save_message(self, message,recipent):
        user_obj = self.user
        receiver = User.objects.get(id=recipent)
        chat_message_obj = ChatMessage.objects.create(
            sender=user_obj,receiver =receiver,  message=message
        )
        return chat_message_obj

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
    
    # @database_sync_to_async
    # def mark_as_delivered(self):
    #     self.status = 'delivered'
    #     self.save()

    # @database_sync_to_async
    # def mark_as_read(self):
    #     self.status = 'read'
    #     self.save()

    # async def send_typing_indicator(self, typing):
    #     # Implement typing indicator logic as needed
    #     pass
