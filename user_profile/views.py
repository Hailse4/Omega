from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView 
from django.views.generic.list import ListView 
from django.views.generic.base import View
from .models import UserProfile
from follow.models import FollowModel
from django.core.serializers import serialize 
from post.models import PostModel 
from .forms import ProfileForm 
from django.http import HttpResponseForbidden, HttpResponse 
from django.contrib.auth.mixins import LoginRequiredMixin 
import json



class ProfilePage(LoginRequiredMixin,DetailView):
    login_url = reverse_lazy('login')
    model = UserProfile 
    context_object_name = "profile_obj"
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs) 
        profile_obj = context['profile_obj']
        current_user_pro = UserProfile.objects.get(user=self.request.user)
        following = serialize('json',[profile_obj])
        follower = serialize('json',[current_user_pro])
        obj_exist = FollowModel.objects.filter(
            follower=follower,following=following).exists()
        if obj_exist:
            state = "unfollow"
        else:
            state = "follow"
        if self.request.user == profile_obj.user:
            own_profile = True
        else:
            own_profile = False
        context['own_profile'] = own_profile
        context['current_user_pro'] = current_user_pro.id
        posts = PostModel.objects.filter(profile=profile_obj)
        context['posts'] = posts
        context['state'] = state
        context['post_count'] = len(posts)
        return context 
    
    
class UpdateProfile(LoginRequiredMixin,UpdateView):
    model = UserProfile
    login_url = reverse_lazy('login')
    form_class = ProfileForm
    def dispatch(self,*args,**kwargs):
        profile = UserProfile.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            if self.request.user != profile.user:
                return HttpResponseForbidden("<h2>403 Forbidden</h2>")
        return super().dispatch(*args,**kwargs)
    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('profile',args=(pk,))
    




    




