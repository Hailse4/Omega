from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import FollowModel,ConfirmFollow
from django.core.serializers import deserialize 

@receiver(post_save,sender=FollowModel)
def create_confirm(sender,instance,created,*args,**kwargs):
    if created:
        print("created")
        follower = list(deserialize("json",instance.follower))[0].object
        following = list(deserialize('json',instance.following))[0].object
        exist = FollowModel.objects.filter(
            follower=instance.following,
            following=instance.follower
        ).exists()
        if exist:
            obj = ConfirmFollow.objects.get(owner=follower,profile=following)
            obj.delete()
        elif not exist:
            ConfirmFollow.objects.create(owner=following,profile=follower)
            


@receiver(post_delete,sender=FollowModel)
def delete_confirm(sender,instance,*args,**kwargs):
    follower = list(deserialize('json',instance.follower))[0].object
    following = list(deserialize ('json',instance.following))[0].object
    exist = ConfirmFollow.objects.filter(
        owner=following, profile=follower
    ).exists()
    if exist:
        obj = ConfirmFollow.objects.get(owner=following,profile=follower)
        obj.delete()
            