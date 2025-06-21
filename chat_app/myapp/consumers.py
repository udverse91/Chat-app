import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

from collections import defaultdict

# Room-wise user tracking (shared across consumers)
active_users_per_room = defaultdict(set)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        self.username = self.scope['url_route']['kwargs']['username']  # Pass username in route

        # Add user to room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Add to active user list
        active_users_per_room[self.room_name].add(self.username)

        # Broadcast updated user list
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'user_list_update',
                'users': list(active_users_per_room[self.room_name])
            }
        )

    async def disconnect(self, close_code):
        # Remove from active user list
        active_users_per_room[self.room_name].discard(self.username)

        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

        # Broadcast updated user list
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'user_list_update',
                'users': list(active_users_per_room[self.room_name])
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender = data.get('sender')
        room_name = data.get('room_name')

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_message',
                'message': {
                    'sender': sender,
                    'message': message,
                    'room_name': room_name,
                }
            }
        )

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        await self.send(text_data=json.dumps({'message': data}))

    async def user_list_update(self, event):
        # Send active user list to frontend
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))

    @database_sync_to_async
    def create_message(self, data):
        try:
            room = Room.objects.get(room_name=data['room_name'])
        except Room.DoesNotExist:
            return
        if not Message.objects.filter(room=room, message=data['message']).exists():
            Message.objects.create(
                room=room,
                sender=data['sender'],
                message=data['message']
            )
