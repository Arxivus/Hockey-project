from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'mobile_phone', 'gender', 'age', 'category', 'rating', 'role']

class loginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)