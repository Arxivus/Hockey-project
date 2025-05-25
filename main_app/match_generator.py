from itertools import combinations, product
from .models import TournamentGroup, Competitor
from .players_functions import splitByRole



def getBalancedTeams(processed_roles, team_comp, top_n):
    best_teams, best_diff = [[], []], 2 ** 20
    top_by_role = {role: players[:top_n] for role, players in processed_roles.items()}

    role_combinations = []
    for role, count in team_comp.items(): # генерация всех комбинаций для team1 по количеству игроков на роли
        role_combinations.append(list(combinations(top_by_role[role], count)))

    for team1_players in product(*role_combinations):  # декартово произведение
        team1 = []
        for role_group in team1_players:
            for player in role_group:
                team1.append(player)
        
        remaining_players = {}
        team2 = []
        for role, players in processed_roles.items(): # формирование team2 из оставшихся игроков
            remaining_players[role] =  [p for p in players if p not in team1]

        for role, count in team_comp.items():
            team2.extend(remaining_players[role][:count])  # берем топ игроков из кол-ва игроков на роли
        
        team1_rt = sum(p['rating'] for p in team1)
        team2_rt = sum(p['rating'] for p in team2)
        rt_diff = abs(team1_rt - team2_rt)

        if rt_diff < best_diff:
            best_diff = rt_diff
            best_teams = [team1, team2, team1_rt + team2_rt]
  
    return best_teams


def getFromPlayed(act_players, players, ages, age_diff, pl_needed):
    additional = []
    for player in players:
        if len(additional) == pl_needed: # добираем до количества на роли
            break
        if (player not in act_players):
            pl_age = player['age']
            if abs(pl_age - min(ages)) <= age_diff and  abs(pl_age - max(ages)) <= age_diff:
                additional.append(player)
    return additional


def getTeamsForMatch(key_age, players_by_role, age_diff, team_comp):
    #param players_by_role: {'role': [player1, player2, ...], ...}
    #param team_composition: {'defender': 2, 'goalkeeper': 1, 'forward': 1})
    processed_roles = {}
    match_ages = [key_age]
    top_n = 3  # ограничение выбора игроков для оптимизации

    for role, role_players in players_by_role.items():
        filtered = []
        for pl in role_players:
            matches_played = pl['matches_played']
            pl_age = pl['age']
            if matches_played < 20: # фильтрация игроков (<20 матчей)
                if abs(pl_age - min(match_ages)) <= age_diff and abs(pl_age - max(match_ages)) <= age_diff:
                    filtered.append(pl)
                
        if (filtered == [] and team_comp[role]!= 0) or len(filtered) < team_comp[role] * 2:
            needed = team_comp[role] * 2 - len(filtered)
            addition = getFromPlayed(filtered, role_players, match_ages, age_diff, needed) # добираем из отыгравших
            filtered = sorted(list(filtered) + list(addition), key=lambda x: (x['matches_played'], x['age']))
            
        processed_roles[role] = filtered
    
    return getBalancedTeams(processed_roles, team_comp, top_n)

# ------------------------------------------------------------------------------------------------------------


def generateMatch(pl_list):
    groups = TournamentGroup.objects.order_by('group_id').all()
    for group in groups:
        if group.stopped_played:
            continue

        else:
            id = group.group_id
            players = Competitor.objects.filter(group_id=id).values()

            if players == None or len(players) < 8:
                print('not enough players in group', id)
                continue

            pl_list = list(players)

            if group.group_age_pool[1] <= 10:
                team_composition = {'forward': 2, 'defender': 2, 'goalkeeper': 0, }
                pl_in_team = 4
            else:
                team_composition = {'forward': 3, 'defender': 2, 'goalkeeper': 1}
                pl_in_team = 6

            forwards, defenders, goalkeepers = splitByRole(pl_list)

            fw_sorted = sorted(forwards, key=lambda x: (x['matches_played'], x['age'], x['rating'])) 
            df_sorted = sorted(defenders, key=lambda x: (x['matches_played'], x['age'], x['rating'])) 
            gk_sorted = sorted(goalkeepers, key=lambda x: (x['matches_played'], x['age'], x['rating'])) 
            players_by_role = {'forward': fw_sorted, 'defender': df_sorted, 'goalkeeper': gk_sorted} 

            less_matches = 10000
            less_matches_age = 0
            for key, role_pls in players_by_role.items():
                if role_pls != []:
                    pl = role_pls[0]         # игрок с наим. количеством матчей
                    if pl['matches_played'] < less_matches:
                        less_matches = pl['matches_played']
                        less_matches_age = pl['age']

            if less_matches < 20:
                try:
                    best_teams = getTeamsForMatch(
                        less_matches_age,
                        players_by_role, 
                        group.age_spread, 
                        team_composition
                    )
                except:
                    print('balancer error')

            else:
                print('All in group played their matches')
                group.stopped_played = True
                group.save()
                continue

            return (best_teams, pl_in_team)

# -------------------------------------------------------------------------------------------------------------------------------------

def getMatchObject(id, team1, team2, pl_in_team):
   
    team1_fw, team1_df, team1_gk = splitByRole(team1)
    team2_fw, team2_df, team2_gk = splitByRole(team2)
    ratings_sum = 0
    for player in list(team1) + list(team2):
        ratings_sum += player['rating']

    match = {
        'match_id': id,
        'matchRating': round(ratings_sum / (pl_in_team * 2)),
                    
        'team1_players' : {
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team1_df],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team1_fw]
        },

        'team2_players' : {
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team2_df],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team2_fw]
        },

        'team1_score' : 0,
        'team2_score' : 0,
    }

    if pl_in_team != 4:
        match['team1_players']['Вратарь'] = [{'id': g['player_id'], 'name': g['name'], 'rate': g['rating']} for g in team1_gk]
        match['team2_players']['Вратарь'] = [{'id': g['player_id'], 'name': g['name'], 'rate': g['rating']} for g in team2_gk]

    return match
