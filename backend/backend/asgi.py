"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from ..EcoQuest import consumers

application = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/notifications/<int:id>/', consumers.NotificationConsumer.as_asgi()),
    ]),
})
