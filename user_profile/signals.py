from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver 
from django.contrib.auth.models import User
from .models import UserProfile
import json

@receiver(post_save,sender=User)
def create_user_profile(sender, instance,created,*args,**kwargs):
    if created:
        UserProfile.objects.create(user=instance,name=instance.username)
    else:
        print("user Does not created")
        
        


            



  

