from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
