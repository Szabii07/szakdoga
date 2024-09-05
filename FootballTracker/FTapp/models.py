# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

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
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    pass

class PlayerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, default=None)
    birthdate = models.DateField(verbose_name="Születési idő")
    team = models.CharField(max_length=255, verbose_name="Csapatnév")
    position = models.CharField(max_length=255, verbose_name="Pozíció")
    preferred_foot = models.CharField(max_length=10, choices=[('left', 'Bal'), ('right', 'Jobb'), ('two', 'Kétlábas')], verbose_name="Milyen lábas", default='right')
    height = models.IntegerField(verbose_name="Magasság")
    location = models.CharField(max_length=255, verbose_name="Tartózkodási hely")
    looking_for_team = models.BooleanField(default=False, verbose_name="Keres csapatot?")
    experience = models.TextField(blank=True, verbose_name="Tapasztalatok")

    def __str__(self):
        return f'{self.team} - {self.position}'

class Coach(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField()
    team = models.CharField(max_length=100)
    qualifications = models.TextField()

    def __str__(self):
        return self.user.user.username
    
class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField()
    team = models.CharField(max_length=100)
    experience = models.TextField()

    def __str__(self):
        return self.user.user.username

class Post(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Following(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)