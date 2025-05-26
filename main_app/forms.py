from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            "username": "Логин",
        }

class profileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'mobile_phone', 'gender', 'age', 'category', 'role']
        labels = {
            "fullname": "ФИО",
            "email": "Email",
            "mobile_phone": "Телефон",
            "gender": "Пол",
            "age": "Возраст",
            "category": "Уровень подготовки", 
            "role": "Роль игрока"
        } 

class loginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100)