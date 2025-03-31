from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    mobile_phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()
    category = models.CharField(max_length=100)
    rating = models.IntegerField(null=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname