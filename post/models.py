from django.db import models
from user_profile.models import UserProfile 
from django.contrib.auth.models import User

class PostModel(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    description = models.TextField(max_length=100)
    image = models.ImageField(upload_to="posts")
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    like = models.IntegerField(default=0,blank=True)
    comment = models.IntegerField(default=0,blank=True)


class LikeCount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    state = models.CharField(max_length=10)

class CommentModel(models.Model):
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    class Meta:
        ordering = ['-id']