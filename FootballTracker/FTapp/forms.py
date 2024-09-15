from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, PlayerProfile, Coach, Manager, Post, Message, Experience, Comment

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
            'first_name': 'Keresztnév',
            'last_name': 'Vezetéknév',
            'email': 'Email cím',
            'role': 'Szerep',
            'avatar': 'Profilkép'
        }

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ['birthdate', 'team', 'position', 'preferred_foot', 'height', 'location', 'looking_for_team']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'position': forms.HiddenInput(),  # Hidden field to be populated by JavaScript
            'preferred_foot': forms.Select(choices=[('left', 'Bal'), ('right', 'Jobb'), ('two', 'Kétlábas')])
        }
        labels = {
            'birthdate': 'Születési idő',
            'team': 'Csapatnév',
            'position': 'Pozíciók',
            'preferred_foot': 'Milyen lábas',
            'height': 'Magasság',
            'location': 'Tartózkodási hely',
            'looking_for_team': 'Keres csapatot?',
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description']
        labels = {
            'title': 'Csapat',
            'description': 'Elért eredmény',
        }

class CoachForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Coach
        fields = ['birthdate', 'team', 'qualifications']
        widgets = {
            'qualifications': forms.HiddenInput(),
        }
        labels = {
            'birthdate': 'Születési idő',
            'team': 'Csapat',
            'qualifications': 'Képesítések',
        }
    
    def clean_qualifications(self):
        qualifications = self.cleaned_data.get('qualifications')
        if qualifications:
            qualifications_list = [q.strip() for q in qualifications.split(',') if q.strip()]
            return ', '.join(qualifications_list)
        return ''



class ManagerForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    players = forms.ModelMultipleChoiceField(queryset=PlayerProfile.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Manager
        fields = ['birthdate', 'players']
        labels = {
            'birthdate': 'Születési idő',
            'players': 'Játékosok',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'Poszt tartalma'
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
        fields = ['recipient', 'content']
        labels = {
            'recipient': 'Címzett',
            'content': 'Üzenet'
        }