from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            "username": "Логин:",
            "password1": "Пароль:",
            "password2": "Подтверждение пароля:"
        }

class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'mobile_phone', 'gender', 'age', 'category', 'rating', 'role']
        labels = {
            "fullname": "Введите ФИО:",
            "email": "Email:",
            "mobile_phone": "Телефон:",
            "gender": "Пол:",
            "age": "Возраст:",
            "category": "Разряд:",
            "rating": "Рейтинг:",
            "role": "Роль(участник/тренер/судья):"
        }

class loginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100)