from django import forms
from .models import UserProfile 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        labels = {'image':"Profile Image",'bio':'Add a bio'}
        widgets = {'name':forms.TextInput(attrs={"placeholder":"Name"}),
                  'bio':forms.Textarea(attrs={'placeholder':'write your bio'})}
        help_texts = {'name':'50 chars','bio':'100 chars'}
        
        