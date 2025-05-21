from .models import TournamentGroup, Competitor

def getTeamPlayersId(team):
    players_id = []
    del team['total_rating']
    roles_players_arr = team.values()
    
    for roles_players in roles_players_arr:
        for player in roles_players:
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



def generateGroups(tournament, age_groups):
    for group_num, age_pool, gender_letter in age_groups:
        spread = 1
        if age_pool[0] == 14:
            spread = 2
        elif age_pool[0] == 17:
            spread = 100

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


def splitByRole(pl_list): 
    forwards, defenders, goalkeepers  = [], [], []
    for pl in pl_list:
        match pl['role']:
            case 'forward': forwards.append(pl)
            case 'defender': defenders.append(pl)
            case 'goalkeeper': goalkeepers.append(pl)

    return forwards, defenders, goalkeepers