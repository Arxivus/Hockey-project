from itertools import combinations
from .models import TourGroupPlayer, Competitor

def addPlayerToGroup(tournament, group_id, group_age_pool, group_gender, player):
    TourGroupPlayer.objects.create(
        tournament = tournament,
        group_id = group_id,
        group_age_pool = group_age_pool,
        group_gender = group_gender,
        player = player
    )

def splitIntoGroups(tournament, players):
    age_groups = [(1, (7, 10)), (2, (11, 13)), (3, (14, 16)), (4, (17, 99))]
    
    for player in players:
        age, gender = player.age, player.gender
        for group_num, (min_age, max_age) in age_groups:
            if min_age <= age <= max_age:
                addPlayerToGroup(tournament, group_num, (min_age, max_age), gender, player)


def splitByRole(pl_list): 
    forwards, defenders, goalkeepers  = [], [], []
    for pl in pl_list:
        match pl['role']:
            case 'forward': forwards.append(pl)
            case 'defender': defenders.append(pl)
            case 'goalkeeper': goalkeepers.append(pl)

    return forwards, defenders, goalkeepers

# ------------------------------------------------------------------------------------------------------------------------------

def getBalancedTeams(fw_sorted, df_sorted, gk_sorted, pl_in_team):
    # Выбираем вратарей с наименьшим количеством матчей
    best_diff = float('inf')
    best_teams = []
    fw_in_team = round(pl_in_team / 2)
    have_gk = len(gk_sorted) != 0 
    
    # Берем т8 нападающих и 6 защитников (для оптимизации)
    top_fw = fw_sorted[:8]
    top_df = df_sorted[:6]

    for fw_combo in combinations(top_fw, fw_in_team * 2):
        for df_combo in combinations(top_df, 4):
            # Формируем команды
            team1_fw, team2_fw = fw_combo[:fw_in_team], fw_combo[fw_in_team:]
            team1_df, team2_df = df_combo[:2], df_combo[2:]
            rating1, rating2 = 0, 0
            
            if have_gk:
                team1_gk, team2_gk = [gk_sorted[0]], [gk_sorted[1]]
                rating1 += gk_sorted[0]['rating']
                rating2 += gk_sorted[1]['rating']

            rating1 += sum(p['rating'] for p in team1_fw) + sum(p['rating'] for p in team1_df)
            rating2 += sum(p['rating'] for p in team2_fw) + sum(p['rating'] for p in team2_df)
            
            diff = abs(rating1 - rating2)
            
            if diff < best_diff:
                best_diff = diff

                if have_gk:
                    best_teams = [
                        {'goalkeeper': team1_gk, 'defenders': team1_df, 'forwards': team1_fw, 'total_rating': rating1},
                        {'goalkeeper': team2_gk, 'defenders': team2_df, 'forwards': team2_fw, 'total_rating': rating2}
                    ]
                else:
                    best_teams = [
                        {'defenders': team1_df, 'forwards': team1_fw, 'total_rating': rating1},
                        {'defenders': team2_df, 'forwards': team2_fw, 'total_rating': rating2}
                    ]
                
                if best_diff == 0:
                    break
    return best_teams


def generateMatch(pl_list):
    youngest_group_pl = TourGroupPlayer.objects.order_by('group_id').first()

    if youngest_group_pl is None:
        return (None, None)

    else:
        id = youngest_group_pl.group_id
        players_ids = TourGroupPlayer.objects.filter(group_id = id).values_list('player_id', flat=True)
        players = Competitor.objects.filter(player_id__in=players_ids).values()
        pl_list = list(players)
        pl_in_team = 6

        if id == 1:
            pl_in_team = 4

        forwards, defenders, goalkeepers = splitByRole(pl_list)

        fw_sorted = sorted(forwards, key=lambda x: (x['matches_played'], x['rating']))
        df_sorted = sorted(defenders, key=lambda x: (x['matches_played'], x['rating']))
        gk_sorted = sorted(goalkeepers, key=lambda x: (x['matches_played'], x['rating']))
        

        best_teams = getBalancedTeams(fw_sorted, df_sorted, gk_sorted, pl_in_team)
        return (best_teams, pl_in_team)

# -------------------------------------------------------------------------------------------------------------------------------------

def getMatchObject(id, team1, team2, pl_in_team):
    match = {
        'match_id': id,
        'matchRating': round((team1['total_rating'] + team2['total_rating']) / (pl_in_team * 2)),
                    
        'team1_players' : {
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team1['defenders']],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team1['forwards']]
        },

        'team2_players' : {
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team2['defenders']],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team2['forwards']]
        },

        'team1_score' : 0,
        'team2_score' : 0,
    }

    if pl_in_team != 4:
        match['team1_players']['Вратарь'] = [{'id': g['player_id'], 'name': g['name'], 'rate': g['rating']} for g in team1['goalkeeper']]
        match['team2_players']['Вратарь'] = [{'id': g['player_id'], 'name': g['name'], 'rate': g['rating']} for g in team2['goalkeeper']]

    return match


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
        print(len(matrix))
        for other_id in all_match_id:
            if (other_id in team1_playersId and id in team1_playersId) or (other_id in team2_playersId and id in team2_playersId):
                matrix[id][other_id][0] += 1
            else:
                matrix[id][other_id][1] += 1
        print(2)
    tournament.played_with_matrix = matrix
    tournament.save() 