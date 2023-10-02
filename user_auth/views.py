from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic.list import ListView 
from django.contrib import messages
from user_profile.models import UserProfile
from post.models import PostModel 
from django.http import HttpResponse, HttpResponseRedirect 


@login_required(login_url=reverse_lazy('login'),redirect_field_name='next')
def home(request):
    response = HttpResponse("<h1>Home Page</h1>")
    response['Content-Type'] = 'text/html'
    return response 

class LoginPage(LoginView):
    redirect_authenticated_user = True
    template_name = 'user_auth/login.html'
    fields = ['username','password']
    def get_success_url(self):
        return reverse_lazy('home')


class SignupPage(FormView):
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    template_name = "user_auth/sign-up.html"
    def post(self, request,*args,**kwargs):
        data = {'username': request.POST['username'],
                'email': request.POST['email'],
                'password1': request.POST['password1'],
                'password2': request.POST['password2']}
        f_data = UserCreationForm(data)
        form = f_data
        if f_data.is_valid():
            f_data.cleaned_data['password'] = f_data.cleaned_data['password1']
            del f_data.cleaned_data['password1']
            del f_data.cleaned_data['password2']
            User.objects.create_user(**f_data.cleaned_data)
            messages.success(request,'account created successfully')
            return redirect(reverse_lazy('login'))
        else:
            print("Form is not valid")
            return super().form_invalid(form)


class HomeView(ListView):
    model = PostModel
    template_name = 'user_auth/home.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.request.user.is_authenticated:
            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile
        return context 
            