from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'profile_picture','bio']

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ('username', 'email', 'password1', 'password2') 
