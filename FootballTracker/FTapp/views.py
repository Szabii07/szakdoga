import json
from django.views.decorators.csrf import csrf_exempt
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q, Prefetch
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.signals import post_save
from .forms import SignupForm, LoginForm, UserProfileForm, CoachForm, ManagerForm, PostForm, PlayerProfileForm, CommentForm, MessageForm
from .models import Dislike, Like, UserProfile, PlayerProfile, Coach, Manager, Post, Message, Comment, Team, Note
import logging
logger = logging.getLogger(__name__)


def index_view(request):
    signup_form = SignupForm(auto_id='signup_%s')  
    login_form = LoginForm(auto_id='login_%s')    

    if request.method == "POST":
        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                messages.success(request, 'Sikeres regisztráció! Kérlek, szerkeszd a profilodat.')
                return redirect('create_user_profile')
            else:
                messages.error(request, 'Sikertelen regisztráció. Kérlek, ellenőrizd az adatokat.')

        elif 'login' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                try:
                    profile = UserProfile.objects.get(user=user)
                    role = profile.role
                    if role == 'player':
                        return redirect('player_dashboard')
                    elif role == 'coach':
                        return redirect('coach_dashboard')
                    elif role == 'manager':
                        return redirect('manager_dashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, 'Profil nem található.')
                    return redirect('create_user_profile')
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
            form = PlayerProfileForm(request.POST, request.FILES, instance=user_profile.playerprofile)
        elif user_profile.role == 'coach':
            form = CoachForm(request.POST, request.FILES, instance=user_profile.coach)
        elif user_profile.role == 'manager':
            form = ManagerForm(request.POST, request.FILES, instance=user_profile.manager)
        
        if form and form.is_valid():
            form.save()
            messages.success(request, 'Profil sikeresen mentve!')
            return redirect('dashboard_redirect')
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
        form = UserProfileForm(request.POST, request.FILES)
        logger.info(f"FILES: {request.FILES}")
        if form.is_valid():
            user = request.user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                user_profile.first_name = form.cleaned_data['first_name']
                user_profile.last_name = form.cleaned_data['last_name']
                user_profile.email = form.cleaned_data['email']
                user_profile.role = form.cleaned_data['role']

                if request.FILES.get('avatar'):
                    logger.info(f"Avatar uploaded: {request.FILES['avatar']}")
                    user_profile.avatar = request.FILES['avatar']
                else:
                    logger.warning("No avatar uploaded")

                user_profile.save()

            role = form.cleaned_data['role']
            if role == 'player':
                return redirect('create_player_profile')
            elif role == 'coach':
                return redirect('create_coach_profile')
            elif role == 'manager':
                return redirect('create_manager_profile')
            else:
                return redirect('dashboard_redirect')
    else:
        form = UserProfileForm()

    return render(request, 'create_user_profile.html', {'form': form})


@role_required('player')
@login_required
def create_player_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
<<<<<<< HEAD
        form = PlayerProfileForm(request.POST)
        if form.is_valid():
            player_profile = form.save(commit=False)
            player_profile.user_profile = user_profile
=======
        profile_form = PlayerProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            player_profile = profile_form.save(commit=False)
            try:
                player_profile.user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                messages.error(request, "Nincs felhasználói profil.")
                return redirect('create_player_profile')

            # Csapatlétrehozás/update
            team_name = profile_form.cleaned_data.get('team_name').strip()
            if team_name:
                team, created = Team.objects.get_or_create(name=team_name)
                player_profile.team = team
            else:
                player_profile.team = None
>>>>>>> ea9aa5dc1c2b5424f1fb71ac9fb60f3459e0801c
            
            # Team creation/update logic
            team_choice = form.cleaned_data.get('team_choice')
            team_name = form.cleaned_data.get('team_name')

            player_profile.save()

<<<<<<< HEAD
            if team_choice:
                # Use selected team
                team = team_choice
            elif team_name:
                # Create a new team
                team, created = Team.objects.get_or_create(name=team_name)
            else:
                team = None

            if team:
                team.players.add(player_profile)  # Add player to the team
                player_profile.team_name = team.name  # Optionally store the team name in player profile
                player_profile.save()

=======
>>>>>>> ea9aa5dc1c2b5424f1fb71ac9fb60f3459e0801c
            # Pozíciók
            positions = request.POST.get('position', '').split(',')
            player_profile.position = ','.join(positions)
            player_profile.save()

            # Játékos csapathoz való hozzáadása
            if player_profile.team:
                player_profile.team.players.add(player)

            return redirect('player_dashboard')
        else:
            print(profile_form.errors)
    else:
        profile_form = PlayerProfileForm()
    
    return render(request, 'create_player_profile.html', {'form': profile_form})

@role_required('coach')
@login_required
def create_coach_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coach = form.save(commit=False)
            coach.user = user_profile
            
            # Csapat létrehozása/frissítése
            team_choice = form.cleaned_data.get('team_choice')
            team_name = form.cleaned_data.get('team_name')

            coach.save()
            
            if team_choice:
                # Kiválasztott csapat használata
                team = team_choice
            elif team_name:
                # Új csapat létrehozása
                team, created = Team.objects.get_or_create(name=team_name)
            else:
                team = None

            if team:
                team.coach = coach
                team.save()
                coach.team = team
                coach.save()

            messages.success(request, 'Coach profile created/updated successfully!')
            return redirect('coach_dashboard')
    else:
        existing_coach = Coach.objects.filter(user=user_profile).first()
        form = CoachForm(instance=existing_coach) if existing_coach else CoachForm()

    return render(request, 'create_coach_profile.html', {'form': form})



@role_required('manager')
@login_required
def create_manager_profile_view(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        
        # Kiválasztott játékosok ID-i
        selected_players_ids = request.POST.get('players', '').split(',')

        print("Selected Player IDs:", selected_players_ids)

        if form.is_valid():
            manager = form.save(commit=False)
            manager.user = request.user.userprofile
            manager.save()

            # Játékosok lekérdezése és hozzárendelése
            selected_players = PlayerProfile.objects.filter(id__in=selected_players_ids)
            manager.players.set(selected_players)
            manager.save()

            return redirect('manager_dashboard')
    else:
        form = ManagerForm()

    return render(request, 'create_manager_profile.html', {'form': form})




def search_players(request):
    query = request.GET.get('q', '')
    players = PlayerProfile.objects.filter(user_profile__first_name__icontains=query)
    player_list = [{'id': player.id, 'first_name': player.user_profile.first_name, 'last_name': player.user_profile.last_name} for player in players]
    return JsonResponse({'players': player_list})

@role_required('player')
@login_required
def player_dashboard(request):
    player_profile = PlayerProfile.objects.get(user_profile__user=request.user)
    teamName = player_profile.team_name
    team = Team.objects.get(name=teamName)

<<<<<<< HEAD
    try:
        team = Team.objects.get(name=teamName)
    except Team.DoesNotExist:
        team = None

=======
>>>>>>> ea9aa5dc1c2b5424f1fb71ac9fb60f3459e0801c
    posts = Post.objects.all().order_by('-created_at')

    # Csapattagok kigyűjtése
    team_players = PlayerProfile.objects.filter(team_name=teamName).exclude(user_profile__user=request.user)
    coaches = Coach.objects.filter(team=team)

    conversation_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    context = {
        'posts': posts,
        'post_form': PostForm(),
        'comment_form': CommentForm(),
        'team': team,
        'team_players': team_players,
        'coaches': coaches,
        'conversation_users': conversation_users,
    }

    # Posztok kezelése
    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('player_dashboard')
        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return redirect('player_dashboard')

    return render(request, 'player_dashboard.html', context)

@role_required('coach')
@login_required
def coach_dashboard(request):
    posts = Post.objects.all().order_by('-created_at')

    try:
        coach = Coach.objects.get(user=request.user.userprofile)  # Coach profil lekérése
        team = coach.team  # Coach csapatának lekérése
        team_players = PlayerProfile.objects.filter(team_name=team.name)
        team_coaches = Coach.objects.filter(team=team).exclude(user=request.user.userprofile)
    except Coach.DoesNotExist:
        coach = None
        team = None
        team_players = []
        team_coaches = []

    conversation_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    context = {
        'posts': posts,
        'post_form': PostForm(),
        'comment_form': CommentForm(),
        'team': team,
        'team_players': team_players,
        'team_coaches':team_coaches,
        'conversation_users': conversation_users,
    }

    # Posztok kezelése
    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('coach_dashboard')
        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return redirect('coach_dashboard')

    return render(request, 'coach_dashboard.html', context)

@role_required('manager')
@login_required
def manager_dashboard(request):
    existing_players = []
    try:
        manager = Manager.objects.get(user=request.user.userprofile)
        team_players = manager.players.all()
        
        # Meglévő játékosok lekérdezése, akik nem tagjai a menedzsernek
        existing_players = PlayerProfile.objects.exclude(id__in=team_players.values_list('id', flat=True))

    except Manager.DoesNotExist:
        team_players = []
        existing_players = PlayerProfile.objects.all()  # Ha nincs menedzser, minden játékos elérhető, de ez kizárt, mivel role_requirednek menedzser van megadva

    # Korábbi emberek lekérdezése, akikkel beszélgetett már
    conversation_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'post_form': PostForm(),
        'comment_form': CommentForm(),
        'team_players': team_players,
        'existing_players': existing_players,
        'conversation_users': conversation_users,
    }

    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('manager_dashboard')

        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                return redirect('manager_dashboard')

    return render(request, 'manager_dashboard.html', context)



@login_required
def user_filter(request):
    user_type = request.GET.get('user_type')
    players = PlayerProfile.objects.all()
    coaches = Coach.objects.all()
    managers = Manager.objects.all()
    teams = Team.objects.all()
    
    if user_type == 'player':
        min_height = request.GET.get('min_height')
        max_height = request.GET.get('max_height')
        min_birth_date = request.GET.get('min_birth_date')
        max_birth_date = request.GET.get('max_birth_date')
        position = request.GET.get('position')
        preferred_foot = request.GET.get('preferred_foot')
        location = request.GET.get('location')
        looking_for_team = request.GET.get('looking_for_team')
        team_name = request.GET.get('team_name')
        

        if min_height:
            players = players.filter(height__gte=min_height)
        if max_height:
            players = players.filter(height__lte=max_height)
        if min_birth_date:
            players = players.filter(birthdate__gte=min_birth_date)
        if max_birth_date:
            players = players.filter(birthdate__lte=max_birth_date)
        if position:
            position_filter = Q()
            positions = position.split(',')
            for pos in positions:
                position_filter |= Q(position__icontains=pos)
            players = players.filter(position_filter)
        if preferred_foot:
            players = players.filter(preferred_foot=preferred_foot)
        if location:
            players = players.filter(location__icontains=location)
        if looking_for_team:
            players = players.filter(looking_for_team=looking_for_team)
        if team_name:
            players = players.filter(team_name=team_name)

        context = {
            'players': players,
            'coaches': None,
            'managers': None,
            'teams': teams,
        }
    elif user_type == 'coach':
        context = {
            'players': None,
            'coaches': coaches,
            'managers': None,
            'teams': teams,
        }
    elif user_type == 'manager':
        context = {
            'players': None,
            'coaches': None,
            'managers': managers,
            'teams': teams,
        }
    else:
        context = {
            'players': None,
            'coaches': None,
            'managers': None,
            'teams': teams,
        }
    
    return render(request, 'user_filter.html', context)



@login_required
def redirect_to_dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role == 'player':
        return redirect('player_dashboard')
    elif user_profile.role == 'coach':
        return redirect('coach_dashboard')
    elif user_profile.role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('index')

@login_required
def create_post_player(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('player_dashboard')
    else:
        form = PostForm()
    
    return render(request, 'create_post_player.html', {'form': form})


@login_required
def profile_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)

    # Bejelentkezett felhasználó követi-e
    is_following = user_profile in request.user.userprofile.following.all()

    try:
        player_profile = PlayerProfile.objects.get(user_profile=user_profile)
    except PlayerProfile.DoesNotExist:
        player_profile = None

    try:
        coach_profile = Coach.objects.get(user=user_profile)
    except Coach.DoesNotExist:
        coach_profile = None

    try:
        manager_profile = Manager.objects.get(user=user_profile)
    except Manager.DoesNotExist:
        manager_profile = None

    if not player_profile and not coach_profile and not manager_profile:
        return render(request, 'profile_not_found.html')

    context = {
        'user_profile': user_profile,
        'player_profile': player_profile,
        'coach_profile': coach_profile,
        'manager_profile': manager_profile,
        'is_following': is_following,
    }

    return render(request, 'profile_detail.html', context)

@login_required
def my_follows(request):
    followed_users = request.user.userprofile.following.all()

    context = {
        'followed_users': followed_users
    }
    
    return render(request, 'my_follows.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.save()
            return redirect('messages', user_id=request.user.id)
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})

@login_required
def messages_overview(request):
    # Lekérdezi azokat a felhasználókat, akikkel a bejelentkezett felhasználó beszélgetett
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).distinct()
    
    # Kiválasztja azokat a felhasználókat, akikkel a bejelentkezett felhasználó beszélgetett
    # figyelembe véve, hogy az ő saját üzeneteit ne jelenítse meg
    users = User.objects.filter(
        Q(sent_messages__in=conversations) | Q(received_messages__in=conversations)
    ).exclude(id=request.user.id).distinct()
    
    context = {
        'users': users,
    }
    
    return render(request, 'messages_overview.html', context)

@login_required
def conversation_view(request, user_id):
    selected_user = get_object_or_404(User, id=user_id)
    
    # Üzenetek lekérése a bejelentkezett és a kiválasztott ember között
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=selected_user)) |
        (Q(sender=selected_user) & Q(recipient=request.user))
    ).order_by('created_at')
    
    # Emberek lekérése
    conversation_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = selected_user
            new_message.save()
            return redirect('conversation_view', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'selected_user': selected_user,
        'messages': messages,
        'form': form,
        'conversation_users': conversation_users,
    }
    return render(request, 'conversation_view.html', context)

@login_required
def new_conversation_view(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        if recipient_id:
            return redirect('conversation_view', user_id=recipient_id)
    else:
        users = User.objects.exclude(id=request.user.id)
    
    context = {
        'users': users,
    }
    return render(request, 'new_conversation.html', context)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(UserProfile, pk=user_id)
    current_user_profile = request.user.userprofile

    if current_user_profile != user_to_follow:  # Magát ne tudja követni
        current_user_profile.following.add(user_to_follow)

    # Követi-e
    if user_to_follow not in request.user.userprofile.following.all():
        request.user.userprofile.following.add(user_to_follow)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(UserProfile, pk=user_id)
    current_user_profile = request.user.userprofile

    if current_user_profile != user_to_unfollow:  # Magát ne tudja követni
        current_user_profile.following.remove(user_to_unfollow)
    
    # Megnézzük h követi-e, mielőtt kikövetnénk
    if user_to_unfollow in request.user.userprofile.following.all():
        request.user.userprofile.following.remove(user_to_unfollow)

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = Post(user=request.user, content=content, image=image)
        post.save()
        return redirect('dashboard_redirect')
    return redirect('dashboard_redirect')

@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Ha már dislikeolta
    if Dislike.objects.filter(post=post, user=user).exists():
        # Ha igen, tűnjön el
        Dislike.objects.filter(post=post, user=user).delete()

    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:  # Ha már likeolta, tűnjön el
        like.delete()
        liked = False
    else:
        liked = True

    # Számláló update
    like_count = post.get_likes_count()
    dislike_count = post.get_dislikes_count()

    return JsonResponse({
        'success': True,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'liked': liked,
    })

@require_POST
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Ha már likeolta
    if Like.objects.filter(post=post, user=user).exists():
        # Ha igen, tűnjön el
        Like.objects.filter(post=post, user=user).delete()

    dislike, created = Dislike.objects.get_or_create(post=post, user=user)
    if not created:  # Ha dislikeolta, tűnjön el
        dislike.delete()
        disliked = False
    else:
        disliked = True

    # Számláló update
    like_count = post.get_likes_count()
    dislike_count = post.get_dislikes_count()

    return JsonResponse({
        'success': True,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'disliked': disliked,
    })

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

def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

#Manager profil létrehozásához
def get_player_name(request):
    player_id = request.GET.get('id')
    try:
        player = PlayerProfile.objects.get(id=player_id)
        name = f"{player.user_profile.first_name} {player.user_profile.last_name}"
        return JsonResponse({'name': name})
    except PlayerProfile.DoesNotExist:
        return JsonResponse({'name': 'Nincs ilyen játékos'}, status=404)
    
#Manager dashboardhoz
@login_required
def add_existing_player(request):
    if request.method == 'POST':
        player_id = request.POST.get('player')
        next_url = request.GET.get('next', 'manager_dashboard')

        try:
            player = PlayerProfile.objects.get(id=player_id)
            manager = Manager.objects.get(user=request.user.userprofile)
            manager.players.add(player)
            messages.success(request, "A játékos sikeresen hozzáadva.")
        except PlayerProfile.DoesNotExist:
            messages.error(request, "A kiválasztott játékos nem található.")
        except Manager.DoesNotExist:
            messages.error(request, "Menedzser profil nem található.")

        return redirect(next_url)
    

@role_required('manager')
@login_required
def my_players(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.role == 'manager':
        try:
            manager_instance = Manager.objects.get(user=user_profile)

            # Manager játékosainak lekérése
            players = PlayerProfile.objects.filter(managers=manager_instance).prefetch_related(
                Prefetch('notes', queryset=Note.objects.filter(manager=manager_instance))
            )

            # Nem a manager játékosainak lekérése
            existing_players = PlayerProfile.objects.exclude(managers=manager_instance)
        except Manager.DoesNotExist:
            players = PlayerProfile.objects.none()
            existing_players = PlayerProfile.objects.all()
    else:
        players = PlayerProfile.objects.none()
        existing_players = PlayerProfile.objects.none()

    return render(request, 'my_players.html', {
        'players': players,
        'existing_players': existing_players
    })


@login_required
def save_note(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        note_text = request.POST.get('note')

        try:
            manager = Manager.objects.get(user=request.user.userprofile)
            player = PlayerProfile.objects.get(id=player_id)

            note = Note.objects.create(player=player, manager=manager, text=note_text)

            return JsonResponse({'note_id': note.id, 'note': note.text})
        except (PlayerProfile.DoesNotExist, Manager.DoesNotExist):
            return JsonResponse({'error': 'Player or Manager not found'}, status=404)

@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        note = Note.objects.get(id=note_id)
        note.delete()
        return JsonResponse({'status': 'success'})

@role_required('manager')
@login_required
def remove_player(request, player_id):
    user_profile = request.user.userprofile

    if user_profile.role == 'manager':
        manager = get_object_or_404(Manager, user=user_profile)
        player = get_object_or_404(PlayerProfile, id=player_id)

        manager.players.remove(player)

    return redirect('my_players')

@login_required
def custom_logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('index')