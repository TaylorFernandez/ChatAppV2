"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from communication.consumers import GlobalChatConsumer, ChatroomConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

asgi_application = get_asgi_application()

#define routing between http methods and websockets
application = ProtocolTypeRouter({
    'http': asgi_application,
    "websocket": AllowedHostsOriginValidator(
        URLRouter([
            path("chat/", GlobalChatConsumer.as_asgi()),
            path("chat/room/", ChatroomConsumer.as_asgi())
        ])
    ),
})
