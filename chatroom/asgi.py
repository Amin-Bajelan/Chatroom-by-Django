"""
ASGI config for chatroom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatroom.routing import websocket_urlpatterns  # وارد کردن مسیرهای WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatroom.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # درخواست‌های HTTP به سرور معمولی Django می‌روند
    "websocket": AuthMiddlewareStack(  # WebSocket‌ها به کانال‌ها هدایت می‌شوند
        URLRouter(
            websocket_urlpatterns  # مسیرهای WebSocket که در routing.py تعریف می‌کنید
        )
    ),
})