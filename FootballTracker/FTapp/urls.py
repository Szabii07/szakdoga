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

from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'),
    path('create_player_profile/', views.create_player_profile, name='create_player_profile'),
    path('create_coach_profile/', views.create_coach_profile, name='create_coach_profile'),
    path('create_manager_profile/', views.create_manager_profile_view, name='create_manager_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('follow_player/<int:player_id>/', views.follow_user, name='follow_player'),
    path('player_dashboard/', views.player_dashboard, name='player_dashboard'),
    path('coach_dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('send_message/', views.send_message, name='send_message'),
    path('create_post/', views.create_post, name='create_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('messages/<int:user_id>/', views.messages_view, name='messages'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
