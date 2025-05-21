from itertools import combinations
from .models import TournamentGroup, Competitor
from .players_functions import splitByRole


def getBalancedTeams(fw_sorted, df_sorted, gk_sorted, pl_in_team):
    best_diff = float('inf')
    best_teams = []
    fw_in_team = round(pl_in_team / 2)
    have_gk = len(gk_sorted) != 0 
    
    # Берем т8 нападающих и т6 защитников (для оптимизации)
    top_fw = fw_sorted[:8]
    top_df = df_sorted[:6]

    for fw_combo in combinations(top_fw, fw_in_team * 2):
        for df_combo in combinations(top_df, 4):
            
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
    groups = TournamentGroup.objects.order_by('group_id').all()
    for group in groups:
        if group.stopped_played:
            continue

        else:
            id = group.group_id
            players = Competitor.objects.filter(group_id=id).values()

            if players == None or len(players) < 8:
                print('not enough players in', id)
                continue

            pl_list = list(players)

            if group.group_age_pool[1] <= 10:
                pl_in_team = 4
            else:
                pl_in_team = 6

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
