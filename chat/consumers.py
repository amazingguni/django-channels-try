import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        qs = parse_qs(self.scope['query_string'].decode('utf-8'))
        if 'token' not in qs:
            return
        token = qs['token'][0]
        user_id = cache.get(f'{token}')
        self.room_group_name = f'chat_{user_id}'
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def push(self, event):
        print('push')
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
