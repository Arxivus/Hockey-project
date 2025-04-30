from django.contrib import admin
from .models import Profile, TestBalancer, Micromatch, Announsment

admin.site.register(Profile)
admin.site.register(TestBalancer)
admin.site.register(Micromatch)
admin.site.register(Announsment)