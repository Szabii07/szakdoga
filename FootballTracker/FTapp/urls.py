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
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'),
    path('create_player_profile/', views.create_player_profile, name='create_player_profile'),
    path('create_coach_profile/', views.create_coach_profile, name='create_coach_profile'),
    path('create_manager_profile/', views.create_manager_profile_view, name='create_manager_profile'),
    path('player_dashboard/', views.player_dashboard, name='player_dashboard'),
    path('coach_dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('create_post/', views.create_post, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('messages/', views.messages_overview, name='messages_overview'),
    path('messages/<int:user_id>/', views.conversation_view, name='conversation_view'),
    path('messages/new/', views.new_conversation_view, name='new_conversation'),
    path('send_message/', views.send_message, name='send_message'),
    path('user_filter/', views.user_filter, name='user_filter'),
    path('create_post_player/', views.create_post_player, name='create_post_player'),
    path('dashboard_redirect/', views.redirect_to_dashboard, name='dashboard_redirect'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('koveteseim/', views.my_follows, name='my_follows'),
    path('search_players/', views.search_players, name='search_players'),
    path('get_player_name/', views.get_player_name, name='get_player_name'),
    path('add-existing-player/', views.add_existing_player, name='add_existing_player'),
    path('remove_player/<int:player_id>/', views.remove_player, name='remove_player'),
    path('my_players/', views.my_players, name="my_players"),
    path('save_note/', views.save_note, name='save_note'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

