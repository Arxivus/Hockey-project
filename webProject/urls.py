from django.contrib import admin
from django.urls import path, include
from main_app import views 

urlpatterns = [
    path('', views.home_page, name='home'),
    path('timetable/', views.timetable_page, name='timetable'),
    path('timetable/get-matches/', views.get_stored_matches_view, name='get_stored_matches'),
    path('user/', views.user_profile, name='user'),
    path('user/edit-profile/', views.user_edit_profile, name='user_edit_profile'),
    path('tournaments/', views.tournaments_page, name='tournaments'),
    path('tournaments/reg-in-tour', views.register_to_tournament, name='register_to_tour'),
    path('tournaments/check-register/', views.check_register, name='check_register'),
    path('tournaments/start-new/', views.start_new_tour_view, name='start_new_tour'),
    path('tournaments/get-next-match/<int:group_id>', views.get_next_match_view, name='get_next_match'),
    path('tournaments/check-permissions/', views.get_user_permissions, name='get_user_permissions'),
    path('tournaments/get-stored-matches/', views.get_stored_matches_view, name='get_stored_matches'),
    path('tournaments/save-match/<uuid:match_id>/', views.save_match_view, name='save_match'),
    path('tournaments/shift-matches-time/', views.shift_matches_view, name='shift_matches'),
    path('ratings/', views.ratings_page, name='ratings'),
    path('ratings/get-competitors/', views.get_competitors_view, name='get_competitors'),
    path('admin/', admin.site.urls, name='admin:index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
]
