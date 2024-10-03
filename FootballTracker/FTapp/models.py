# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_ROLES = [
        ('player', 'Játékos'),
        ('coach', 'Edző'),
        ('manager', 'Menedzser'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, default='example@example.com')
    role = models.CharField(max_length=10, choices=[('player', 'Játékos'), ('coach', 'Edző'), ('manager', 'Menedzser')])
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_set', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    pass

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.OneToOneField('Coach', on_delete=models.SET_NULL, related_name='coached_team', null=True, blank=True)
    players = models.ManyToManyField('PlayerProfile', related_name='teams')
    def __str__(self):
        return self.name

class PlayerProfile(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Kapus'),
        ('RB', 'Jobbhátvéd'),
        ('CB', 'Középhátvéd'),
        ('LB', 'Balhátvéd'),
        ('CDM', 'Védekező középpályás'),
        ('CM', 'Középpályás'),
        ('CAM', 'Támadó középpályás'),
        ('RW', 'Jobbszélső'),
        ('LW', 'Balszélső'),
        ('ST', 'Csatár'),
        ('CF', 'Középcsatár')
    ]
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, default=None)
    birthdate = models.DateField(verbose_name="Születési idő")
    team_name = models.CharField(max_length=255, verbose_name="Csapatnév", null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.TextField(verbose_name="Pozíciók")
    preferred_foot = models.CharField(max_length=10, choices=[('left', 'Bal'), ('right', 'Jobb'), ('two', 'Kétlábas')], verbose_name="Milyen lábas", default='right')
    height = models.IntegerField(verbose_name="Magasság")
    location = models.CharField(max_length=255, verbose_name="Tartózkodási hely")
    looking_for_team = models.BooleanField(default=False, verbose_name="Keres csapatot?")

    def __str__(self):
        return f'{self.team_name} - {self.position}'
    

class Coach(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name="Születési idő")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='coach_profile')
    qualifications = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name="Születési idő")
    team = models.CharField(max_length=100, null=True)
    experience = models.TextField()
    players = models.ManyToManyField(PlayerProfile, blank=True, related_name='managers')

    def __str__(self):
        return self.user.user.username
    
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follows', on_delete=models.CASCADE)
    followed = models.ForeignKey(UserProfile, related_name='followed_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower} follows {self.followed}'


class Post(models.Model):
    AUDIENCE_CHOICES = [
        ('everyone', 'Everyone'),
        ('coaches', 'Coaches'),
        ('players', 'Players'),
        ('managers', 'Managers'),
        ('team', 'My Team'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='everyone')

    def get_likes_count(self):
        return self.like_set.count()

    def get_dislikes_count(self):
        return self.dislike_set.count()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} at {self.created_at}"

class Note(models.Model):
    text = models.TextField()
    player = models.ForeignKey(PlayerProfile, related_name='notes', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text