from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models.signals import post_save
from .forms import SignupForm, LoginForm, UserProfileForm, CoachForm, ManagerForm, PostForm, MessageForm, PlayerProfileForm  
from .models import UserProfile, PlayerProfile, Coach, Manager, Post, Message, Following, Favorite


def index_view(request):
    signup_form = SignupForm()  
    login_form = LoginForm()    
    
    if request.method == "POST":
        if 'signup' in request.POST:
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Sikeres regisztráció! Kérlek, szerkeszd a profilodat.')
                return redirect('create_user_profile')
            else:
                messages.error(request, 'Sikertelen regisztráció. Kérlek, ellenőrizd az adatokat.')
        elif 'login' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')  # profil szerkesztés helyett a dashboardra
                else:
                    messages.error(request, 'Hibás bejelentkezési adatok.')

    return render(request, 'index.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })

@login_required
def profile_edit_view(request):
    user_profile = request.user.userprofile
    form = None

    if request.method == 'POST':
        if user_profile.role == 'player':
            form = PlayerProfileForm(request.POST, instance=user_profile.playerprofile)
        elif user_profile.role == 'coach':
            form = CoachForm(request.POST, instance=user_profile.coach)
        elif user_profile.role == 'manager':
            form = ManagerForm(request.POST, instance=user_profile.manager)
        
        if form and form.is_valid():
            form.save()
            messages.success(request, 'Profil sikeresen mentve!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Hiba történt a profil mentése közben.')
    else:
        if user_profile.role == 'player':
            form = PlayerProfileForm(instance=user_profile.playerprofile)
        elif user_profile.role == 'coach':
            form = CoachForm(instance=user_profile.coach)
        elif user_profile.role == 'manager':
            form = ManagerForm(instance=user_profile.manager)
    
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Create or update the user profile
            user = request.user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                user_profile.first_name = form.cleaned_data['first_name']
                user_profile.last_name = form.cleaned_data['last_name']
                user_profile.email = form.cleaned_data['email']
                user_profile.role = form.cleaned_data['role']
                user_profile.save()

            # Redirect based on the selected role
            role = form.cleaned_data['role']
            if role == 'player':
                return redirect('create_player_profile')
            elif role == 'coach':
                return redirect('create_coach_profile')
            elif role == 'manager':
                return redirect('create_manager_profile')
            else:
                return redirect('dashboard')  # Fallback if role is not recognized

    else:
        form = UserProfileForm()

    return render(request, 'create_user_profile.html', {'form': form})


@login_required
def create_player_profile(request):
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST)
        if form.is_valid():
            # Get the user's profile
            user_profile = UserProfile.objects.get(user=request.user)

            # Create the player profile and associate it with the user profile
            player_profile = form.save(commit=False)
            player_profile.user_profile = user_profile
            player_profile.save()

            return redirect('player_dashboard')  # Redirect to player dashboard
    else:
        form = PlayerProfileForm()

    return render(request, 'create_player_profile.html', {'form': form})


@login_required
def create_coach_profile_view(request):
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coach_profile = form.save(commit=False)
            coach_profile.user = request.user
            coach_profile.save()
            return redirect('dashboard')
    else:
        form = CoachForm()
    
    return render(request, 'create_coach_profile.html', {'form': form})

@login_required
def create_manager_profile_view(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            manager_profile = form.save(commit=False)
            manager_profile.user = request.user
            manager_profile.save()
            return redirect('dashboard')
    else:
        form = ManagerForm()

    players = PlayerProfile.objects.all()
    return render(request, 'create_manager_profile.html', {'form': form, 'players': players})

@login_required
def player_dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    posts = Post.objects.filter(user_profile=user_profile).order_by('-created_at')
    following_profiles = user_profile.following.all()
    
    if request.method == 'POST':
        if 'post' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user_profile = user_profile
                post.save()
                return redirect('player_dashboard')
        elif 'message' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = user_profile
                message.save()
                return redirect('player_dashboard')
    else:
        post_form = PostForm()
        message_form = MessageForm()

    context = {
        'posts': posts,
        'following_profiles': following_profiles,
        'post_form': post_form,
        'message_form': message_form
    }
    
    return render(request, 'player_dashboard.html', context)

@login_required
def manager_coach_dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role not in ['manager', 'coach']:
        return HttpResponseForbidden("Nem jogosult hozzáférés")

    players = UserProfile.objects.filter(role='player', following=user_profile)
    return render(request, 'manager_coach_dashboard.html', {'players': players})

@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role == 'player':
        followed_users = user_profile.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        return render(request, 'player_dashboard.html', {'posts': posts})
    elif user_profile.role in ['coach', 'manager']:
        players = UserProfile.objects.filter(role='player')
        posts = Post.objects.all()
        return render(request, 'coach_manager_dashboard.html', {'players': players, 'posts': posts})
    else:
        return redirect('index')

@login_required
def view_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, pk=user_id)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def send_message(request, user_id):
    receiver = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.userprofile
            message.receiver = receiver
            message.save()
            return redirect('dashboard')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.userprofile
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(UserProfile, id=user_id)
    request.user.userprofile.following.add(user_to_follow)
    return redirect('dashboard')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(UserProfile, id=user_id)
    request.user.userprofile.following.remove(user_to_unfollow)
    return redirect('dashboard')

@login_required
def add_to_favorites(request, player_id):
    player = get_object_or_404(UserProfile, id=player_id, role='player')
    request.user.userprofile.favorites.add(player)
    return redirect('dashboard')

@login_required
def remove_from_favorites(request, player_id):
    player = get_object_or_404(UserProfile, id=player_id, role='player')
    request.user.userprofile.favorites.remove(player)
    return redirect('dashboard')

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = UserProfile.objects.filter(first_name__icontains=query) | UserProfile.objects.filter(last_name__icontains=query)
    return render(request, 'search_results.html', {'users': users})

@login_required
def search_players(request):
    query = request.GET.get('q', '')
    players = PlayerProfile.objects.filter(team__icontains=query) | PlayerProfile.objects.filter(position__icontains=query)
    return render(request, 'search_results.html', {'players': players})

@login_required
def favorites_list(request):
    favorites = request.user.userprofile.favorites.all()
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def add_favorite(request, player_id):
    player = get_object_or_404(PlayerProfile, id=player_id)
    user_profile = request.user.userprofile
    if not user_profile.favorites.filter(id=player_id).exists():
        user_profile.favorites.add(player)
    return redirect('favorites')

@login_required
def remove_favorite(request, player_id):
    player = get_object_or_404(PlayerProfile, id=player_id)
    user_profile = request.user.userprofile
    if user_profile.favorites.filter(id=player_id).exists():
        user_profile.favorites.remove(player)
    return redirect('favorites')
