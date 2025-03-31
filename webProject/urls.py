from django.contrib import admin
from django.urls import path, include
from main_app import views 

urlpatterns = [
    path('', views.home_page, name='home'),
    path('user/', views.user_profile, name='user'),
    path('tournaments/', views.tournaments_page, name='tournaments'),
    path('about_us/', views.about_us_page, name='about_us'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
