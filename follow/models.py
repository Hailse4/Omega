from django.db import models
from user_profile.models import UserProfile

class FollowModel(models.Model):
    follower = models.JSONField()
    following = models.JSONField()
    appear_in_list = models.BooleanField(default=True,blank=True)
    
    
class ConfirmFollow(models.Model):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    profile = models.ForeignKey(
        UserProfile,on_delete=models.CASCADE,
        related_name="follower"
    )
    