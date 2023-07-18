from django.urls import re_path
from base.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat_room/(?P<room_name>\w+)', ChatRoomConsumer.as_asgi())
]