from django.urls import path
from . import views

urlpatterns = [
    path("account/<int:pk>/",views.ProfilePage.as_view(),name="profile"),
    path("update/<int:pk>/",views.UpdateProfile.as_view(),name='update-profile'),
]
