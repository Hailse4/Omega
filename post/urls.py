from django.urls import path
from . import views

urlpatterns = [
    path('form/',views.CreatePost.as_view(),name="post"),
    path('update/<int:pk>/',views.UpdatePost.as_view(),name="update-post"),
    path('delete/<int:pk>/',views.DeletePost.as_view(),name="delete-post"),
    path("postlike/",views.postlike,name="postlike"),
    path('postdetail/<int:pk>/',views.PostDetail.as_view(),name="postdetail"),
]
