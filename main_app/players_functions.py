from datetime import datetime, timedelta
from .models import TournamentGroup, Competitor, Profile, Micromatch
from django.contrib.auth.decorators import login_required


def isRegister(request):
    profile = Profile.objects.get(user=request.user)
    already_register = Competitor.objects.filter(profile=profile).exists()
    return True if already_register else False

def isEnoughInGroup(players, group):
    if players == None or len(players) < 8: 
        print('not enough players in group', group.group_id)
        group.stopped_played = True 
        group.save()
        return False
    
    return True


def addMinutes(time, minutes):
    dummy_datetime = datetime.combine(datetime.today().date(), time)
    new_datetime = dummy_datetime + timedelta(minutes=minutes)
    return new_datetime.time()


@login_required
def addToCompetitors(request):
    profile = Profile.objects.get(user=request.user)
    fullname = profile.fullname
    split_name = fullname.split()
    fs_name = split_name[0]
    if len(split_name) >= 2:
        fs_name = split_name[0] + ' ' + split_name[1]
    
    rating = 0
    if profile.rating:
        rating = profile.rating
    else:
        match profile.age:
            case int() if profile.age <= 10:
                rating = profile.age * 150
            case int( ) if 11 <= profile.age <= 15:
                rating = 2200
            case int( ) if profile.age >= 16:
                rating = 2500   

    Competitor.objects.create(
        profile=profile,
        name=fs_name,
        age=profile.age,
        role=profile.role,
        gender=profile.gender,
        rating=rating,
        start_rating=rating
    )


def getTeamPlayersId(team):
    players_id = []
    for player in team:
        players_id.append(player['player_id'])
    return players_id



def updatePlayersMatrix(tournament, team1, team2):
    team1_playersId = getTeamPlayersId(team1)
    team2_playersId = getTeamPlayersId(team2)
  
    all_match_id = list(team1_playersId) + list(team2_playersId)
    matrix = tournament.played_with_matrix
    for id in all_match_id:
        player = Competitor.objects.get(player_id=id)
        player.matches_played += 1
        player.save()
        for other_id in all_match_id:
            if (other_id in team1_playersId and id in team1_playersId) or (other_id in team2_playersId and id in team2_playersId):
                matrix[id][other_id][0] += 1
            else:
                matrix[id][other_id][1] += 1
                
    tournament.played_with_matrix = matrix
    tournament.save() 


def getCreationMatchInfo(tournament, group_id):
    last_matches = Micromatch.objects.filter(tournament=tournament, group_id=group_id).order_by('-start_time')[:2]
    last_match = last_matches[0]
    prelast_match = last_matches[1]
    print(last_match, group_id)
    
    match_delay = tournament.minutes_btwn_matches
    match_time = addMinutes(last_match.start_time, 1 + match_delay)
    
    if group_id == 1 or group_id == 2:
        if last_match.field_num == prelast_match.field_num:
            match_field = 1 if last_match.field_num == 2 else 2
        else:
            match_field = last_match.field_num
    else:
        match_field = 1 if last_match.field_num == 2 else 2
    
    return (match_time, match_field)
    
    


def generateGroups(tournament, age_groups):
    TournamentGroup.objects.all().delete()
    
    for group_num, age_pool, gender_letter in age_groups:
        spread = 1
        if age_pool[0] == 11:
            spread = 2
        elif age_pool[0] == 16:
            spread = 80

        TournamentGroup.objects.create(
            tournament = tournament,
            group_id = group_num,
            group_age_pool = age_pool,
            age_spread = spread,
            group_gender = gender_letter
        )


def splitIntoGroups(players, age_groups):
    for player in players:
        age, gender = player.age, player.gender
        for group_num, (min_age, max_age), gender_letter in age_groups:
            if min_age <= age <= max_age and gender == gender_letter:
                player.group_id = group_num
                player.save()
                break


def splitByRole(pl_list): 
    forwards, defenders, goalkeepers  = [], [], []
    for pl in pl_list:
        match pl['role']:
            case 'forward': forwards.append(pl)
            case 'defender': defenders.append(pl)
            case 'goalkeeper': goalkeepers.append(pl)

    return forwards, defenders, goalkeepers