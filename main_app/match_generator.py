import math
from itertools import combinations, product
from .models import TournamentGroup, Competitor, Micromatch, uuid
from .players_functions import splitByRole, updatePlayersMatrix, isEnoughInGroup, addMinutes



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

# -------------------------------------------------------------------------------------------------------------------------

def prepareTeams(group):
    id = group.group_id
    players = Competitor.objects.filter(group_id=id, banned=False).values()

    if not isEnoughInGroup(players, group):
        return ([], 0)

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
    max_matches = -1
    less_matches_age = 0
    for key, role_pls in players_by_role.items():
        if role_pls != []:
            pl_l = role_pls[0]         # игрок с наим. количеством матчей
            pl_m = role_pls[-1]         # игрок с наиб. количеством матчей
            
            if pl_l['matches_played'] < less_matches:
                less_matches = pl_l['matches_played']
                less_matches_age = pl_l['age']
                
            if pl_m['matches_played'] > max_matches:
                max_matches = pl_m['matches_played']

    if less_matches < 20 and max_matches < 25:
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
        return ([], 0)
        
    return (best_teams, pl_in_team)


def generateMatch(group_id): # вызывается после сохранения результата одного из матчей (group_id получать)
    group = TournamentGroup.objects.filter(group_id=group_id).first()
    if group.stopped_played:
        return ([], 0)
    else:
        return prepareTeams(group)

# --------------------------------------------------------------------------------------------------------------

def generateTimetable(tournament): # генерация расписания (первых матчей всех групп)
    groups_ids = tournament.playing_groups_ids
    timetable_matches = [] 
    last_time = tournament.time_started
    group_time_end = last_time
    group_delay = int(tournament.minutes_btwn_groups)
    match_delay = int(tournament.minutes_btwn_matches)
    field_num = 2
    i = 0

    for group_id in groups_ids:
        group = TournamentGroup.objects.filter(group_id=group_id).first()
        pl_in_group = Competitor.objects.filter(group_id=group_id, banned=False).values()
        
        if not isEnoughInGroup(pl_in_group, group) or group.stopped_played:
            continue

        pl_in_team = 6 if group.age_spread > 1 else 4
        formula = (len(pl_in_group) * 10) / (pl_in_team * 2)
        matches_count = math.ceil(formula)
        group_time_end = addMinutes(last_time, ((matches_count * 2) + (matches_count * match_delay))) 
        
        for _ in range(matches_count):
            
            
            if group_id == 1 or group_id == 2: # младшие играют 2 матча на 1-ом поле
                if i % 2 == 0:
                    field_num = 1 if field_num == 2 else 2
                    last_time = addMinutes(last_time, 1 + match_delay)
            else:
                field_num = 1 if field_num == 2 else 2
                last_time = addMinutes(last_time, 1 + match_delay)
            i += 1
            match_time = last_time
            
            teams, pl_in_team = prepareTeams(group)
            match = getSavedMatch(tournament, group_id, match_time, field_num, teams, pl_in_team)
            timetable_matches.append(match)
             
        last_time = addMinutes(group_time_end, group_delay) 
        field_num = 1
        i = 0
  
    return timetable_matches

# -------------------------------------------------------------------------------------------------------------------------------------

def getSavedMatch(tournament, group_id, match_time, field_num, teams, pl_in_team): # сохранение матча в базе
    team1 = teams[0]
    team2 = teams[1]
    match_uniq_id = uuid.uuid4()
    match = getMatchObject(match_uniq_id, group_id, match_time, field_num, team1, team2, pl_in_team)
    updatePlayersMatrix(tournament, team1, team2)
    
    Micromatch.objects.create(
            tournament = tournament,
            group_id = match['group_id'],
            match_id = match['match_id'],
            matchRating = match['match_rating'],
            players_ids = match['players_ids'],
            team1_players = match['team1_players'],
            team2_players = match['team2_players'],
            start_time = match['start_time'],
            field_num = match['field_num']
    )

    return match


def getMatchObject(id, group_id, match_time, field_num, team1, team2, pl_in_team):
   
    team1_fw, team1_df, team1_gk = splitByRole(team1)
    team2_fw, team2_df, team2_gk = splitByRole(team2)
    ratings_sum = 0
    for player in list(team1) + list(team2):
        ratings_sum += player['rating']
    
    all_players = team1 + team2
    players_ids = [pl['player_id'] for pl in all_players]
    
    match = {
        'group_id' : group_id,
        'match_id': id,
        'start_time' : match_time,  
        'field_num' : field_num,
        'match_rating': round(ratings_sum / (pl_in_team * 2)),
        'players_ids' : players_ids,
                    
        'team1_players' : {
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team1_df],
            'Нападающие': [{'id': f['player_id'],'name': f['name'], 'rate': f['rating']} for f in team1_fw]
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
        match['team2_players']['Вратарь'] = [{'id': g['player_id'],'name': g['name'], 'rate': g['rating']} for g in team2_gk]

    return match
