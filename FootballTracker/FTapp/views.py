from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models.signals import post_save
from .forms import SignupForm, LoginForm, UserProfileForm, CoachForm, ManagerForm, PostForm, MessageForm, PlayerProfileForm, ExperienceForm, CommentForm
from .models import Dislike, Follow, Like, UserProfile, PlayerProfile, Coach, Manager, Post, Message, Experience, Comment


def index_view(request):
    signup_form = SignupForm(auto_id='signup_%s')  
    login_form = LoginForm(auto_id='login_%s')    

    if request.method == "POST":
        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)  # Initialize with POST data
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, 'Sikeres regisztráció! Kérlek, szerkeszd a profilodat.')
                return redirect('create_user_profile')
            else:
                messages.error(request, 'Sikertelen regisztráció. Kérlek, ellenőrizd az adatokat.')
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)  # Initialize with POST data
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
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
        # Ellenőrizd a POST adatok
        print("POST adatok:", request.POST)
        
        profile_form = PlayerProfileForm(request.POST)
        if profile_form.is_valid():
            player_profile = profile_form.save(commit=False)
            try:
                player_profile.user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                messages.error(request, "Nincs felhasználói profil.")
                return redirect('create_player_profile')
            player_profile.save()
            
            # Handle experiences (if any)
            experience_titles = request.POST.getlist('experience_title')
            experience_descriptions = request.POST.getlist('experience_description')
            for title, description in zip(experience_titles, experience_descriptions):
                if title and description:
                    Experience.objects.create(
                        title=title,
                        description=description,
                        player_profile=player_profile
                    )
            
            return redirect('player_dashboard')
        else:
            print(profile_form.errors)  # Print form errors to console
    else:
        profile_form = PlayerProfileForm()
    
    return render(request, 'create_player_profile.html', {'form': profile_form})

@login_required
def create_coach_profile(request):
    # Ellenőrizzük, hogy létezik-e UserProfile a jelenlegi felhasználóhoz
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coach = form.save(commit=False)
            coach.user = user_profile
            try:
                # Ellenőrizzük, hogy létezik-e már coach profil
                existing_coach = Coach.objects.get(user=user_profile)
                # Ha létezik, frissítjük
                coach.id = existing_coach.id
            except Coach.DoesNotExist:
                # Ha nem létezik, új létrehozás
                pass
            coach.save()
            messages.success(request, 'Coach profile created/updated successfully!')
            return redirect('coach_dashboard')
    else:
        # Töltse be a formot az esetleges meglévő adatokkal
        try:
            existing_coach = Coach.objects.get(user=user_profile)
            form = CoachForm(instance=existing_coach)
        except Coach.DoesNotExist:
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
def coach_dashboard(request):
    # Get filter parameters from request
    user_type = request.GET.get('user_type')
    min_height = request.GET.get('min_height')
    max_height = request.GET.get('max_height')
    min_birth_date = request.GET.get('min_birth_date')
    max_birth_date = request.GET.get('max_birth_date')
    looking_for_team = request.GET.get('looking_for_team')

    # Filter users based on parameters
    player_profiles = PlayerProfile.objects.all()

    if min_height and max_height:
        player_profiles = player_profiles.filter(height__gte=min_height, height__lte=max_height)
    if min_birth_date and max_birth_date:
        player_profiles = player_profiles.filter(birthdate__gte=min_birth_date, birthdate__lte=max_birth_date)
    if looking_for_team:
        player_profiles = player_profiles.filter(looking_for_team=looking_for_team)

    if user_type == 'player':
        player_profiles = player_profiles
    elif user_type == 'coach':
        player_profiles = PlayerProfile.objects.none()  # Or filter coaches if you have a separate CoachProfile
    elif user_type == 'manager':
        player_profiles = PlayerProfile.objects.none()  # Or filter managers if you have a separate ManagerProfile

    # Get posts and messages
    posts = Post.objects.all().order_by('-created_at')
    messages = Message.objects.filter(recipient=request.user)

    context = {
        'player_profiles': player_profiles,
        'posts': posts,
        'messages': messages
    }
    
    return render(request, 'coach_dashboard.html', context)


@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role == 'player':
        followed_users = user_profile.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        return render(request, 'player_dashboard.html', {'posts': posts})
    elif user_profile.role == 'coach':
        players = UserProfile.objects.filter(role='coach')
        posts = Post.objects.all()
        return render(request, 'coach_dashboard.html', {'players': players, 'posts': posts})
    elif user_profile.role == 'manager':
        players = UserProfile.objects.filter(role='manager')
        posts = Post.objects.all()
        return render(request, 'manager_dashboard.html', {'players': players, 'posts': posts})
    else:
        return redirect('index')

@login_required
def view_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, pk=user_id)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, id=recipient_id)
        content = request.POST.get('message_content')
        message = Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return JsonResponse({'success': True})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(UserProfile, id=user_id)
    Follow.objects.create(user=request.user, followed_user=user_to_follow)
    return JsonResponse({'success': True})

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Handle image file
        post = Post(user=request.user, content=content, image=image)
        post.save()
        return redirect('coach_dashboard')
    return redirect('coach_dashboard')

@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if Like.objects.filter(post=post, user=user).exists():
        return JsonResponse({'success': True, 'like_count': post.get_likes_count(), 'dislike_count': post.get_dislikes_count()})

    Dislike.objects.filter(post=post, user=user).delete()
    Like.objects.create(post=post, user=user)

    return JsonResponse({'success': True, 'like_count': post.get_likes_count(), 'dislike_count': post.get_dislikes_count()})

@require_POST
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if Dislike.objects.filter(post=post, user=user).exists():
        return JsonResponse({'success': True, 'like_count': post.get_likes_count(), 'dislike_count': post.get_dislikes_count()})

    Like.objects.filter(post=post, user=user).delete()
    Dislike.objects.create(post=post, user=user)

    return JsonResponse({'success': True, 'like_count': post.get_likes_count(), 'dislike_count': post.get_dislikes_count()})

@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    content = request.POST.get('content')

    comment = Comment.objects.create(post=post, user=user, content=content)

    return JsonResponse({
        'success': True,
        'comment': {
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@login_required
def messages_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'messages.html', context)