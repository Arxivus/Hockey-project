from django.contrib import admin
from django.urls import path, include
from main_app import views 

urlpatterns = [
    path('', views.home_page, name='home'),
    path('user/', views.user_profile, name='user'),
    path('tournaments/', views.tournaments_page, name='tournaments'),
    path('ratings/', views.ratings_page, name='ratings'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('tournaments/generate-teams/', views.generate_teams_view, name='generate_teams'),
    path('tournaments/get-stored-matches/', views.get_stored_matches_view, name='get_stored_matches'),
    path('tournaments/save-match/<uuid:match_id>/', views.save_match_view, name='save_match'),
]
