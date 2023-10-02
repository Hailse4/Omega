from django.urls import path
from user_auth import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/",views.LoginPage.as_view(),name="login"),
    path("logout/", LogoutView.as_view(template_name='user_auth/logout.html'),name="logout"),
    path("sign-up/",views.SignupPage.as_view(),name="sign-up"),
    path('',views.HomeView.as_view(),name="home"),
]