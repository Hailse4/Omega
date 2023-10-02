from django import forms
from .models import PostModel 


class PostForm(forms.ModelForm):
    description = forms.CharField(max_length=100,min_length=3, widget=forms.Textarea(attrs={'placeholder':"write something about the image"}),label="Image Description",help_text="100 chars")
    image = forms.ImageField(label="Post Image")
    class Meta:
        model = PostModel
        exclude = ['profile','created_at','like','comment']
    