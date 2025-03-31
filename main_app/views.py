from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from .forms import createUserForm, profileForm, loginForm
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, 'home.html')

def tournaments_page(request):
    return render(request, 'tournaments.html')

def about_us_page(request):
    return render(request, 'about_us.html')

def login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = loginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = createUserForm(request.POST)
        profile_form = profileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')
    else:
        form = createUserForm()
        profile_form = profileForm()
        
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form })

@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'user_profile.html', { 'profile': profile })
