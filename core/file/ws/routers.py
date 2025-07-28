from .consumers import SessionConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/session/', SessionConsumer.as_asgi())
]