from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic.base import TemplateView
from django.core.serializers import serialize,deserialize 
from user_profile.models import UserProfile
from django.shortcuts import render
from django.urls import reverse_lazy
from follow.models import FollowModel
from .models import ChatModel 


class ChatListView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = "chat/chatlist.html"
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        json_profile = serialize('json',[profile])
        connected_friends = FollowModel.objects.filter(follower=json_profile)
        connected_profiles = []
        for item in connected_friends:
            data = list(deserialize('json',item.following))[0].object
            connected_profiles.append(data)
        context['connected'] = connected_profiles
        context['profile'] = profile 
        return context
    
class ChatRoom(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'chat/chatroom.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        receiver_id = self.kwargs.get('receiver_id')
        sprofile = UserProfile.objects.get(user=self.request.user)
        rprofile = UserProfile.objects.get(id=receiver_id)
        context['sprofile'] = sprofile
        context['rprofile'] = rprofile
        sender_chat = ChatModel.objects.filter(
            sender=sprofile,receiver=rprofile
        )
        receiver_chat = ChatModel.objects.filter(
            sender=rprofile,receiver=sprofile
        )
        all_chat = sender_chat.union(receiver_chat).order_by('time')
        print(all_chat)
        context['roomname'] = receiver_id
        context['all_chat'] = all_chat
        return context 
    