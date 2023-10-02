from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView , DeleteView 
from django.views.generic.detail import DetailView 
from django.contrib.auth.mixins import LoginRequiredMixin 
from user_profile.models import UserProfile 
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseForbidden
from django.urls import reverse_lazy
from .models import PostModel,LikeCount,CommentModel
from .forms import PostForm



@login_required(login_url=reverse_lazy("login"),redirect_field_name="next")
def postlike(request):
    if request.method == "GET":
      return HttpResponseForbidden("<h1>403 Forbidden</h1>")
    if request.method =="POST":
        user = User.objects.get(id=int(request.POST.get('user')))
        post = PostModel.objects.get(id=int(request.POST.get('post')))
        exist = LikeCount.objects.filter(user=user,post=post).exists()
        print("exists",exist)
        if exist:
           likemodel = LikeCount.objects.get(post=post,user=user)
           print(likemodel.state)
           if likemodel.state == "unlike":
              likemodel.post.like -=1
              likemodel.post.save()
              likemodel.delete()
        else:
           print("creating model")
           likemodel = LikeCount.objects.create(user=user,post=post,state="unlike")
           likemodel.post.like +=1
           likemodel.post.save()
        like_count = len(LikeCount.objects.filter(post=post))
        data = {'likecount':like_count}
        print("like count",like_count)
        return JsonResponse(data=data)

    
class PostDetail(DetailView):
    model = PostModel
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        post = PostModel.objects.get(pk=self.kwargs.get('pk'))
        context['comments'] = CommentModel.objects.filter(post=post)
        return context 
    def post(self,request,*args,**kwargs):
        user = User.objects.get(id=request.POST.get('user'))
        profile = UserProfile.objects.get(user=user)
        post = PostModel.objects.get(id=request.POST.get('post'))
        comment = request.POST.get('comment');
        cmobj = CommentModel.objects.create(profile=profile,post=post, comment=comment)
        post.comment += 1
        post.save()
        cm_no = len(CommentModel.objects.filter(post=post))
        data = {
            'cm_no':cm_no,
            'name':cmobj.profile.name,
            'cmpk':cmobj.id,
            'propk':cmobj.profile.id,
            'comment':cmobj.comment,
            'popk':cmobj.post.id,
            'proimg':cmobj.profile.image.url}
        return JsonResponse(data,safe=False)


class CreatePost(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = PostModel

    form_class = PostForm
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        profile = UserProfile.objects.get(user=self.request.user)
        form.instance.profile = profile
        form.save()
        return super().form_valid(form)
    
    
class UpdatePost(LoginRequiredMixin,UpdateView):
    model = PostModel
    login_url = reverse_lazy('login')
    form_class = PostForm
    def get_success_url(self):
        post = PostModel.objects.get(pk=self.kwargs.get('pk'))
        return reverse_lazy('profile',args=(post.profile.id,))
    
    
class DeletePost (LoginRequiredMixin, DeleteView):
    model = PostModel
    login_url = reverse_lazy('login')
    def get_success_url(self):
        post = PostModel.objects.get(pk=self.kwargs.get('pk'))
        url = reverse_lazy('profile', args=(post.profile.id,))
        return url
    
    
