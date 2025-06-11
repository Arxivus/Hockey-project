import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from .models import Profile, Competitor, Tournament, Micromatch, Announsment, uuid
from .forms import createUserForm, profileForm, loginForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .match_generator import generateMatch, getMatchObject
from .players_functions import splitIntoGroups, updatePlayersMatrix, generateGroups, addToCompetitors, isRegister
from .rating_update import updateRatings, updatMatchPlayersScore

def home_page(request):
    announsments = Announsment.objects.all().values()
    announs_list = list(reversed(announsments)) 
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


def get_user_permissions(request):
    if request.method == 'GET':
        return JsonResponse ({
            'canSaveScore': request.user.has_perm('main_app.can_save_score'),
        })


@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'user_profile.html', { 'profile': profile })

@login_required
def user_edit_profile(request):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        data = json.loads(request.body)
        values = data['newValues']

        profile.role = values[0] if values[0] != '' else profile.role
        profile.email = values[1] if values[1] != '' else profile.email
        profile.mobile_phone = values[2] if values[2] != '' else profile.mobile_phone
        profile.age = values[3] if values[3] != '' else profile.age
        profile.category = values[4] if values[4] != '' else profile.category
        profile.save()
        return JsonResponse ({'status': 'success', 'message': 'Profile saved'})


@login_required
def register_to_tournament(request):
    if isRegister(request):
        return redirect('tournaments')
    else:
        try:
            addToCompetitors(request)
        except:
            print('Cant add')
        return redirect('tournaments')
    
@login_required
def check_register(request):
    if isRegister(request):
        return JsonResponse({ 'status': 'success', 'value': True }) 
    return JsonResponse({ 'status': 'success', 'value': False })


def get_competitors_view(request): # получение списка игроков для таблицы рейтингов
    if request.method == 'GET':
        try:
            competitors = Competitor.objects.all().order_by('-rating').values()
            comp_list = list(competitors)
            return JsonResponse({'status': 'success', 'competitors': comp_list}) 
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def get_stored_matches_view(request): # получение сранее сгенерированных матчей последнего турнира
    if request.method == 'GET':
        last_tournament = Tournament.objects.filter(isEnded=False).order_by('-tour_id').first()
        if last_tournament:
            matches = Micromatch.objects.filter(tournament=last_tournament).order_by('created_at').values()
        else:
            return JsonResponse({'status': 'success', 'matches': []})

        matches_list = list(matches)

        return JsonResponse({'status': 'success', 'matches': matches_list}) 
        

def getSavedMatch(tournament, teams, pl_in_team): # сохранение матча в базе
    matchContainer = []
    team1 = teams[0]
    team2 = teams[1]
    match_uniq_id = uuid.uuid4()
    match = getMatchObject(match_uniq_id, team1, team2, pl_in_team)
    updatePlayersMatrix(tournament, team1, team2)
    matchContainer.append(match)

    Micromatch.objects.create(
            tournament = tournament,
            match_id = match['match_id'],
            matchRating = match['matchRating'],
            team1_players = match['team1_players'],
            team2_players = match['team2_players'],
    )

    return matchContainer

def generateTimetable(): # генерация расписания (в процессе реализации)

    # вернуть разбиение на группы

    teams, pl_in_team = generateMatch(pl_list)
    if pl_in_team is None:
        return JsonResponse({'status': 'error', 'message': 'Tournament has ended'})
            
    matchContainer = getSavedMatch(tournament, teams, pl_in_team)
    return JsonResponse({'status': 'success', 'message': 'New tournament has been started', 'matches': matchContainer}) 


@permission_required('myapp.can_start_tour', raise_exception=True)
def start_new_tour_view(request): # запуск нового турнира  
    if request.method == 'POST':
        try:
            Competitor.objects.update(
                group_id = 0,
                matches_played = 0,
                goals_scored = 0,
                goals_taken = 0,
                rating = F('start_rating')
                #start_rating = F('rating')
            )

            data = json.loads(request.body)
            settings = data['tourSettings']
            age_groups = [
                (1, (7, 10), 'M'), (2, (7, 10), 'W'), 
                (3, (11, 13), 'M'), (4, (11, 13), 'W'), 
                (5, (14, 16), 'M'), (6, (14, 16), 'W'),
                (7, (17, 99), 'M'), (8, (17, 99), 'W'),
            ]
            current_age_groups = [group for group in age_groups if group[0] in settings[1]]

            size = Competitor.objects.all().order_by('-player_id').first().player_id + 1
            played_with_matrix = [ [[0,0] for _  in range(size)] for _ in range(size) ]

            tournament = Tournament.objects.create(
                time_started = datetime.strptime(settings[0], '%H:%M').time(),
                playing_groups_ids = settings[1],
                minutes_btwn_groups = settings[2],
                minutes_btwn_matches = settings[3],
                played_with_matrix = played_with_matrix
            )
            generateGroups(tournament, current_age_groups)
            players = Competitor.objects.all()
            splitIntoGroups(players, age_groups)
            
            #generateTimetable()
            return JsonResponse({'status': 'success', 'message': 'Tournament created'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@permission_required('myapp.can_generate_match', raise_exception=True)
def get_next_match_view(request): # получение следующего матча турнира
    if request.method == 'GET':
        try:
            players = Competitor.objects.all().values()
            pl_list = list(players)
            tournament = Tournament.objects.filter(isEnded=False).order_by('-tour_id').first()

            teams, pl_in_team = generateMatch(pl_list)
            if pl_in_team is None:
                return JsonResponse({'status': 'error', 'message': 'Tournament has ended'})

            matchContainer = getSavedMatch(tournament, teams, pl_in_team)
            return JsonResponse({'status': 'success', 'matches': matchContainer})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

def save_match_view(request, match_id): # сохранение результатов матча, обновление Rt
    if request.method == 'POST':
        try:
            match = Micromatch.objects.get(match_id=match_id)
            data = json.loads(request.body)
            new_score1 = int(data['team1_score'])
            new_score2 = int(data['team2_score'])

            diff_score1 = new_score1 - int(match.team1_score)
            diff_score2 = new_score2 - int(match.team2_score)

            match.team1_score = new_score1
            match.team2_score = new_score2
            match.save()

            team1_playersId = data['team1_playersId']
            team2_playersId = data['team2_playersId']

            tournament = match.tournament

            updatMatchPlayersScore(diff_score1, diff_score2, team1_playersId, team2_playersId)
            updateRatings(tournament, team1_playersId, team2_playersId)

            return JsonResponse({'status': 'success', 'message': 'Match saved'})

        except Micromatch.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Match not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)}, status=500)