from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, ProfileForm

def index_view(request):
    signup_form = SignupForm()  # Inicializálás itt
    login_form = LoginForm()    # Inicializálás itt
    
    if request.method == "POST":
        if 'signup' in request.POST:
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Sikeres regisztráció! Kérlek, szerkeszd a profilodat.')
                return redirect('profile_edit')  # Irányítsd a profil szerkesztési oldalra
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
                    return redirect('profile_edit')  # Irányítsd a profil szerkesztési oldalra
    
    return render(request, 'index.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil sikeresen frissítve!')
            return redirect('profile_edit')
        else:
            messages.error(request, 'A profil frissítése nem sikerült. Kérjük, ellenőrizze az adatokat.')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile_edit.html', {'form': form})
