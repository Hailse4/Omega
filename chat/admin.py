from django.contrib import admin
from .models import ChatModel, LiveChatModel 

admin.site.register(ChatModel)
admin.site.register(LiveChatModel)

