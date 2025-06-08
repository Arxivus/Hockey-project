from django import forms
import re
from django.contrib.auth import authenticate
from .models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class createUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['username'].label = "Логин"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Повторите пароль"

        self.fields['password1'].error_messages = {
            'required': _('Пароль обязателен для заполнения'),  
        }


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже зарегистрирован в системе")
        return username

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
       

class profileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        self.fields['fullname'].widget.attrs.update({'placeholder': 'Иванов Иван Иванович'})
        self.fields['email'].widget.attrs.update({'placeholder': 'test@domain.ru'})
        self.fields['mobile_phone'].widget.attrs.update({'placeholder': '+79999999999'})

    def clean_fullname(self):
        fullname = self.cleaned_data['fullname']
        if len(fullname.split()) < 2:
            raise ValidationError("Введите полное ФИО")
        return fullname
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 6:
            raise ValidationError("Минимальный возраст - 6 лет")
        if age > 80:
            raise ValidationError("Проверьте указанный возраст")
        return age
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Profile.objects.filter(email=email).exists():
            raise ValidationError( "Этот email уже зарегистрирован")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(pattern, email):
            raise ValidationError("Введите корректный email адрес")
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        if Profile.objects.filter(mobile_phone=mobile_phone).exists():
            raise ValidationError( "Этот телефон уже используется")
        if not mobile_phone.startswith('+7'):
            raise ValidationError("Введите номер, начинающийся с +7")
        if len(mobile_phone) != 12 or not mobile_phone[1:].isdigit():
            raise ValidationError("Номер должен содержать 11 цифр после +7")
        return mobile_phone

    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'mobile_phone', 'gender', 'age', 'category', 'role']
        labels = {
            "fullname": "ФИО",
            "email": "Email",
            "mobile_phone": "Телефон",
            "gender": "Пол",
            "age": "Возраст",
            "category": "Разряд", 
            "role": "Роль игрока"
        } 

class loginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100)
    
    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            raise ValidationError("Неверный логин или пароль")
        return cleaned_data