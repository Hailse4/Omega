from django.db import models
from user_profile.models import UserProfile


class ChatModel(models.Model):
    sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(
        UserProfile,on_delete=models.CASCADE,
        related_name='message_receiver'
    )
    def __str__(self):
        name = self.sender.name+"&"+self.receiver.name
        return name
    class Meta:
        get_latest_by = 'time'

        
class LiveChatModel(models.Model):
    state = models.CharField(max_length=10)
    sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    receiver = models.ForeignKey(
        UserProfile,on_delete=models.CASCADE,
        related_name='chat_receiver'
    )