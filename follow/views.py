from django.shortcuts import render
from django.http import JsonResponse
from .models import FollowModel,ConfirmFollow
from user_profile.models import UserProfile 
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView 
from django.core.serializers import serialize,deserialize 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 


@login_required(login_url=reverse_lazy('login'), redirect_field_name="next")
def createFollow(request):
    follower_proid = request.POST.get("follower_proid")
    following_proid = request.POST.get("following_proid")
    remove = request.POST.get("remove")
    cfollower = UserProfile.objects.get(id=follower_proid)
    cfollowing = UserProfile.objects.get(id=following_proid)
    follower = serialize('json', [cfollower])
    following =serialize('json',[cfollowing])
    obj_exist = FollowModel.objects.filter(
        follower=follower,following=following).exists() 
    if remove == "False":
        if not obj_exist:
            FollowModel.objects.create(
                follower=follower,
                following=following,
            )
            state = "unfollow"
        elif obj_exist:
            obj = FollowModel.objects.get(
                follower=follower,following=following
                )
            obj.delete()
            state="follow"
        data = {"state":state,"msg":"started following"}
        return JsonResponse(data=data)
    elif remove == 'True':
        exist = ConfirmFollow.objects.filter(
            owner=cfollower,profile=cfollowing
        ).exists()
        if exist:
            print("Happened")
            obj = ConfirmFollow.objects.get(
                owner=cfollower,profile=cfollowing
            )
            obj.delete()
        data = {"msg":"request removed"}
        return JsonResponse(data=data)
        
    
    
class FriendsView(LoginRequiredMixin,TemplateView):
    template_name = "follow/friends.html"
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        json_profile = serialize('json',[profile])
        pro_list = []
        yfollowers = ConfirmFollow.objects.filter(owner=profile)
        all_pro = UserProfile.objects.all().exclude(user=profile.user)
        all_query1 = FollowModel.objects.filter(following=json_profile)
        all_query2 = FollowModel.objects.filter(follower=json_profile)
        all_query = all_query1 | all_query2
        for item in all_query:
            if item.follower != json_profile:
                pro = list(deserialize('json',item.follower))[0].object 
                pro_list.append(pro)
            if item.following != json_profile:
                pro = list(deserialize('json',item.following))[0].object
                pro_list.append(pro)
        suggest = []
        for item in all_pro:
            if not item in pro_list:
                suggest.append(item)
                
        
        context['suggest'] = list(enumerate(suggest))
        context['yfollowers'] = list(enumerate(yfollowers))
        context['profile'] = profile
        return context 
        
