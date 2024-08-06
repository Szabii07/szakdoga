# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Felhasználónév',
            'password1': 'Jelszó',
            'password2': 'Jelszó megerősítése',
        }
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
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
        help_texts = {
            'username': '',
            'password': '',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'profile_picture': forms.FileInput(),
        }
        labels = {
            'username': 'Felhasználónév',
            'email': 'Email',
            'first_name': 'Keresztnév',
            'last_name': 'Vezetéknév',
        }
