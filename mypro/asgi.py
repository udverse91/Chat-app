"""
ASGI config for mypro project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp import routing

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypro.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    )
})
