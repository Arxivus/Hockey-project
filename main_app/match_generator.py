from itertools import combinations

forwards, defenders, goalkeepers  = [], [], []

def startGenerating(pl_list): # функция для ресета турнира
    """ pl_count = len(pl_list)
    goals_with_matrix = [ [0 for _  in range(pl_count + 1)] for _ in range(pl_count + 1) ] """

    global forwards, defenders, goalkeepers
    forwards, defenders, goalkeepers  = [], [], []

    for pl in pl_list:
        match pl['role']:
            case 'forward': forwards.append(pl)
            case 'defender': defenders.append(pl)
            case 'goalkeeper': goalkeepers.append(pl)

    first_match_teams = generateMatch()
    return first_match_teams


def generateMatch(): 
    fw_sorted = sorted(forwards, key=lambda x: (x['matches_played'], x['rating']))
    df_sorted = sorted(defenders, key=lambda x: (x['matches_played'], x['rating']))
    gk_sorted = sorted(goalkeepers, key=lambda x: (x['matches_played'], x['rating']))
    
    # Выбираем вратарей с наименьшим количеством матчей
    team1_gk, team2_gk = gk_sorted[0], gk_sorted[1]
    
    best_diff = float('inf')
    best_teams = []
    
    # Берем т8 нападающих и 6 защитников (для оптимизации)
    top_fw = fw_sorted[:8]
    top_df = df_sorted[:6]

    print(team1_gk, team2_gk)

    for fw_combo in combinations(top_fw, 6):
        for df_combo in combinations(top_df, 4):
            # Формируем команды
            team1_fw = fw_combo[:3]
            team2_fw = fw_combo[3:]
            
            team1_df = df_combo[:2]
            team2_df = df_combo[2:]
            
            rating1 = team1_gk['rating'] + sum(p['rating'] for p in team1_fw) + sum(p['rating'] for p in team1_df)
            rating2 = team2_gk['rating'] + sum(p['rating'] for p in team2_fw) + sum(p['rating'] for p in team2_df)
            
            diff = abs(rating1 - rating2)
            
            if diff < best_diff:
                best_diff = diff
                best_teams = [
                    {'goalkeeper': team1_gk, 'defenders': team1_df, 'forwards': team1_fw, 'total_rating': rating1},
                    {'goalkeeper': team2_gk, 'defenders': team2_df, 'forwards': team2_fw, 'total_rating': rating2}
                ]
                
                if best_diff == 0:
                    break
    
    return best_teams


def getMatchObject(id, team1, team2):
    match = {
        'match_id': id,
        'matchRating': round((team1['total_rating'] + team2['total_rating']) / 12),
                    
        'team1_players' : {
            'Вратарь': [{'id': team1['goalkeeper']['player_id'], 'name': team1['goalkeeper']['name'], 'rate': team1['goalkeeper']['rating']}],
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team1['defenders']],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team1['forwards']]
        },

        'team2_players' : {
            'Вратарь': [{'id': team2['goalkeeper']['player_id'], 'name': team2['goalkeeper']['name'], 'rate': team2['goalkeeper']['rating']}],
            'Защитники': [{'id': d['player_id'], 'name': d['name'], 'rate': d['rating']} for d in team2['defenders']],
            'Нападающие': [{'id': f['player_id'], 'name': f['name'], 'rate': f['rating']} for f in team2['forwards']]
        },

        'team1_score' : 0,
        'team2_score' : 0,
    }

    return match