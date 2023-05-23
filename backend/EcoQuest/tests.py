from django.test import TestCase


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

# Create your tests here.
import pytest
from channels.testing import WebsocketCommunicator
from .consumers import NotificationConsumer
from channels.routing import URLRouter
from django.urls import re_path




@pytest.mark.asyncio
async def test_chat_consumer():
    application = URLRouter([re_path(r"ws/notifications/(?P<id>\w+)/$", NotificationConsumer.as_asgi())])
    communicator = WebsocketCommunicator(application, "/ws/notifications/1/")
    connected, subprotocol = await communicator.connect()
    assert connected

    # test sending text
    await communicator.send_json_to({"message": "hello"})
    response = await communicator.receive_json_from()
    assert response.get("message") == "hello"

    # close
    await communicator.disconnect()

