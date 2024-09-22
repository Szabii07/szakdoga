from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, PlayerProfile, Coach, Manager, Post, Message, Comment, Team

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Felhasználónév',
            'password1': 'Jelszó',
            'password2': 'Jelszó megerősítése',
        }
        widgets = {
            'password1': forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
            'password2': forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Felhasználónév',
            'password': 'Jelszó',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'role', 'avatar']
        labels = {
            'first_name': 'Vezetéknév',
            'last_name': 'Keresztnév',
            'email': 'Email cím',
            'role': 'Szerep',
            'avatar': 'Profilkép'
        }

class PlayerProfileForm(forms.ModelForm):
    team_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = PlayerProfile
        fields = ['birthdate', 'team_name', 'position', 'preferred_foot', 'height', 'location', 'looking_for_team']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'position': forms.HiddenInput(),  # Hidden field to be populated by JavaScript
            'preferred_foot': forms.Select(choices=[('left', 'Bal'), ('right', 'Jobb'), ('two', 'Kétlábas')])
        }
        labels = {
            'birthdate': 'Születési idő',
            'team_name': 'Csapatnév',
            'position': 'Pozíciók',
            'preferred_foot': 'Milyen lábas',
            'height': 'Magasság',
            'location': 'Tartózkodási hely',
            'looking_for_team': 'Keres csapatot?',
        }

class CoachForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    team_name = forms.CharField(max_length=100, required=False, label="Csapatnév")
    team_choice = forms.ModelChoiceField(queryset=Team.objects.all(), required=False, label="Válassz csapatot")

    class Meta:
        model = Coach
        fields = ['birthdate', 'team_name', 'team_choice', 'qualifications']
        widgets = {
            'qualifications': forms.HiddenInput(),
        }
        labels = {
            'birthdate': 'Születési idő',
            'team_name': 'Csapatnév (új)',
            'team_choice': 'Csapatválasztó',
            'qualifications': 'Képesítések',
        }
    
    def clean_team_name(self):
        team_name = self.cleaned_data.get('team_name')
        if team_name:
            team, created = Team.objects.get_or_create(name=team_name)
            return team
        return None

    def clean_team_choice(self):
        team = self.cleaned_data.get('team_choice')
        return team



class ManagerForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    team = forms.CharField(label="Csapatnév", required=False)
    
    class Meta:
        model = Manager
        fields = ['birthdate', 'team']
        labels = {
            'birthdate': 'Születési idő',
            'team': 'Csapatnév',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'audience']
        widgets = {
            'audience': forms.Select(choices=Post.AUDIENCE_CHOICES),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Szólj hozzá...', 'rows': 3}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': 'Üzenet',
        }