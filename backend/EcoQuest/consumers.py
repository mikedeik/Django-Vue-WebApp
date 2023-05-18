from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['id']
        user = await self.get_user_by_id()

        if user is None:
            await self.close()
        else:
            self.user = user
            self.user_group = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )

    async def notify(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def get_user_by_id(self):
        try:
            return User.objects.get(id=self.id)
        except User.DoesNotExist:
            return None
