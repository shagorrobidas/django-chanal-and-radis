import json
from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    WebsocketConsumer
)
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer

 
class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        self.send(text_data=json.dumps({
            'status': 'connected form django channels',
        }))

    def receive(self, text_data):
        print("Received data:", text_data)
        self.send(text_data=json.dumps({
            'status': 'received from django channels',
            'data': text_data
        }))

    def disconnect(self, *args, **kwargs):
        print("Disconnected from test consumer")

    def send_notification(self, event):
        print("Sending notification:")
        data = json.loads(event.get('data'))
        self.send(text_data=json.dumps({'payload': data}))
        print("Notification sent to test consumer")


class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = "new_consumer"
        self.room_group_name = "new_consumer_group"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'status': 'connected to new consumer'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected from new consumer")

    async def receive(self, text_data):
        print("Received data in new consumer:", text_data)
        await self.send(text_data=json.dumps({
            'status': 'received in new consumer',
            'data': text_data
        }))

    async def disconnect(self, *args, **kwargs):
        print("Disconnected from test consumer")

    async def send_notification(self, event):
        print("Sending notification:")
        data = json.loads(event.get('data'))
        await self.send(text_data=json.dumps({'payload': data}))
        print("Notification sent to test consumer")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Broadcast message to group
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
