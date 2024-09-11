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
    team = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    pass

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
    team = models.CharField(max_length=255, verbose_name="Csapatnév")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    preferred_foot = models.CharField(max_length=10, choices=[('left', 'Bal'), ('right', 'Jobb'), ('two', 'Kétlábas')], verbose_name="Milyen lábas", default='right')
    height = models.IntegerField(verbose_name="Magasság")
    location = models.CharField(max_length=255, verbose_name="Tartózkodási hely")
    looking_for_team = models.BooleanField(default=False, verbose_name="Keres csapatot?")
    experience = models.TextField(blank=True, verbose_name="Tapasztalatok")

    def __str__(self):
        return f'{self.team} - {self.position}'

class Experience(models.Model):
    title = models.CharField(max_length=255, verbose_name="Cím")
    description = models.TextField(verbose_name="Leírás")
    player_profile = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='experiences')

    def __str__(self):
        return self.title

class Coach(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name="Születési idő")
    team = models.CharField(max_length=100)
    qualifications = models.TextField()

    def __str__(self):
        return self.user.user.username
    
class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name="Születési idő")
    team = models.CharField(max_length=100)
    experience = models.TextField()

    def __str__(self):
        return self.user.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} követi {self.followed_user.username}"