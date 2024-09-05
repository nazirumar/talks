import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talks.settings')

django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from vcall.routing import websocket_urlpatterns as vcall_websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    chat_websocket_urlpatterns + vcall_websocket_urlpatterns
                )
            )
        ),
    }
)
