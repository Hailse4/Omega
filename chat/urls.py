from django.urls import path
from . import views


urlpatterns = [
    path("chatlist/",views.ChatListView.as_view(),name="chatlist"),
    path("chatroom/<int:receiver_id>/",views.ChatRoom.as_view(),name="chatroom"),
]