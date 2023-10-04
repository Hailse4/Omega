from django.urls import path 
from . import consumers 

websocket_urlpatterns = [
    path('ws/chat/<str:receiver_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/livechat/<str:room_name>/', consumers.LiveChatConsumer.as_asgi()),
]