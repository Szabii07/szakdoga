"""
URL configuration for FootballTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'),
    path('create_player_profile/', views.create_player_profile, name='create_player_profile'),
    path('create_coach_profile/', views.create_coach_profile_view, name='create_coach_profile'),
    path('create_manager_profile/', views.create_manager_profile_view, name='create_manager_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('add_to_favorites/<int:player_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:player_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search/', views.search_users, name='search_users'),
    path('follow_player/<int:player_id>/', views.follow_user, name='follow_player'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('favorites/add/<int:player_id>/', views.add_favorite, name='add_favorite'),
    path('player_dashboard/', views.player_dashboard, name='player_dashboard'),
    path('manager_coach_dashboard/', views.manager_coach_dashboard, name='manager_coach_dashboard'),
]
