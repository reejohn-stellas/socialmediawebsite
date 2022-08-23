from socket import fromshare
from django import forms
from .models import Post,Comment,Profile

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['text','image']

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_pic','cover_pic','bio','location']


