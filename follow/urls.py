from django.urls import path
from . import views

urlpatterns = [
    path("",views.createFollow,name="follow"),
    path("friends/",views.FriendsView.as_view(),name="friends"),
]