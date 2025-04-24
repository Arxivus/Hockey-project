from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, TestBalancer
from .forms import createUserForm, profileForm, loginForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .team_generator import generate_teams

def home_page(request):
    return render(request, 'home.html')

def tournaments_page(request):
    return render(request, 'tournaments.html')

def ratings_page(request):
    competitors = Profile.objects.all().order_by('-rating')
    return render(request, 'ratings.html', { 'competitors' : competitors })

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


def get_competitors(request):
    if request.metod == 'POST':
        competitors = Profile.objects.all()
        return render(request, 'ratings.html', { 'competitors' : competitors })



def generate_teams_view(request):
    if request.method == 'GET':
        try:
            players = TestBalancer.objects.all().values()
            pl_list = list(players)
            teams = generate_teams(pl_list)
            
            teams_data = []
            for team in teams:
                teams_data.append({
                    'total_rating': team['total_rating'],
                    'goalkeeper': {'name': team['goalkeeper']['name'], 'rate': team['goalkeeper']['rating']},
                    'defenders': [{'name': d['name'], 'rate': d['rating']} for d in team['defenders']],
                    'forwards': [{'name': f['name'], 'rate': f['rating']} for f in team['forwards']]
                })
            
            return JsonResponse({
                'status': 'success',
                'teams': teams_data
            }) #list(players)
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)