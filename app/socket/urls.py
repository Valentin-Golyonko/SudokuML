from django.urls import path

from app.socket.socket_scripts.consumers import ChatConsumer

websocket_urls = [
    path("ws/solver/", ChatConsumer.as_asgi(), name="solver"),
]
