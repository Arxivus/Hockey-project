import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Competitor, Tournament, Micromatch, Announsment, uuid
from .forms import createUserForm, profileForm, loginForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .match_generator import startGenerating, generateMatch, getMatchObject
from .rating_update import updateRatings, updateGoalsMatrix

def home_page(request):
    announsments = Announsment.objects.all().values()
    announs_list = list(announsments) 
    return render(request, 'home.html', {'announs_list' : announs_list})

def tournaments_page(request):
    return render(request, 'tournaments.html')

def ratings_page(request):
    return render(request, 'ratings.html')

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


def get_competitors_view(request):
    if request.method == 'GET':
        try:
            competitors = Profile.objects.all().order_by('-rating').values()
            comp_list = list(competitors)
            return JsonResponse({'status': 'success', 'competitors': comp_list}) 
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_stored_matches_view(request): 
    if request.method == 'GET':
        #matches = Micromatch.objects.all().order_by('created_at').values()
        last_tournament = Tournament.objects.order_by('-tour_id').first()
        if last_tournament:
            matches = Micromatch.objects.filter(tournament=last_tournament).order_by('created_at').values()
        else:
            return JsonResponse({'status': 'error', 'message': 'Matches not found'}, status=404)

        matches_list = list(matches)

        return JsonResponse({'status': 'success', 'matches': matches_list}) 
        

def getSavedMatch(tournament, teams): 
    matchContainer = []
    team1 = teams[0]
    team2 = teams[1]
    match_uniq_id = uuid.uuid4()
    match = getMatchObject(match_uniq_id, team1, team2)
    matchContainer.append(match)

    Micromatch.objects.create(
            tournament = tournament,
            match_id = match['match_id'],
            matchRating = match['matchRating'],
            team1_players = match['team1_players'],
            team2_players = match['team2_players'],
    )

    return matchContainer


def generate_teams_view(request): # запуск нового турнира
    if request.method == 'GET':
        try:
            players = Competitor.objects.all().values()
            pl_list = list(players)
            pl_count = len(pl_list)
            print(pl_list)
            goals_with_matrix = [ [0 for _  in range(pl_count + 1)] for _ in range(pl_count + 1) ]

            tournament = Tournament.objects.create(goal_matrix = goals_with_matrix)
            
            teams = startGenerating(pl_list)
            matchContainer = getSavedMatch(tournament, teams)
        
            return JsonResponse({'status': 'success', 'matches': matchContainer})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_next_match_view(request): # следующий матч турнира
    if request.method == 'GET':
        try:
            teams = generateMatch()
            tournament = Tournament.objects.last()
            matchContainer = getSavedMatch(tournament, teams) #------------------------------------------------------
            return JsonResponse({'status': 'success', 'matches': matchContainer})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

def save_match_view(request, match_id):
    if request.method == 'POST':
        try:
            match = Micromatch.objects.get(match_id=match_id)
            data = json.loads(request.body)
            score1 = data['team1_score']
            score2 = data['team2_score']

            match.team1_score = score1
            match.team2_score = score2
            match.save()

            team1_playersId = data['team1_playersId']
            team2_playersId = data['team2_playersId']

            updateGoalsMatrix(score1, score2, team1_playersId, team2_playersId)
            updateRatings(score1, score2, team1_playersId, team2_playersId)

            return JsonResponse({'status': 'success', 'message': 'Match saved'})

        except Micromatch.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Match not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)}, status=500)