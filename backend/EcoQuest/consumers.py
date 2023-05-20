from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("trying connection")
        self.id = self.scope['url_route']['kwargs']['id']
        print(self.id)
        print(self.channel_layer)
        user = await self.get_user_by_id()

        if user is None:
            print("closing")
            await self.close()
        else:
            self.user = user
            self.user_group = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )

            await self.accept()

            self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'you are connected'
            }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )

    async def receive(self, text_data=None):

        text_data = json.loads(text_data)
        message = text_data['message']

        async_to_sync(self.channel_layer.group_send)(
            self.user_group,
            {
                'type': 'message',
                'message': message
            }
        )

    async def message(self, event):
        print("it notifies")
        await self.send(text_data=json.dumps(event['data']))
        # await self.send(text_data=json.dumps({{id: 1, message: test}})
    @database_sync_to_async
    def get_user_by_id(self):
        try:
            return User.objects.get(id=self.id)
        except User.DoesNotExist:
            return None
