import random

def generate_teams(players):
    forwards, defenders, goalkeepers  = [], [], []

    for pl in players:
        match pl['role']:
            case 'forward': forwards.append(pl)
            case 'defender': defenders.append(pl)
            case 'goalkeeper': goalkeepers.append(pl)
    
    teams = balance_teams(forwards, defenders, goalkeepers)
    optimize_teams(teams)
    
    return teams


def balance_teams(forwards, defenders, goalkeepers):
    num_teams = min(len(goalkeepers), len(defenders)//2, len(forwards)//3)
    teams = []
    
    sorted_forwards = sorted(forwards, key=lambda x: -x['rating'])
    sorted_defenders = sorted(defenders, key=lambda x: -x['rating'])
    sorted_goalkeepers = sorted(goalkeepers, key=lambda x: -x['rating'])
  
    for i in range(num_teams):
        gk = sorted_goalkeepers[i]

        def1 = sorted_defenders[i*2]
        def2 = sorted_defenders[i*2 + 1]

        fw1 = sorted_forwards[i*3]
        fw2 = sorted_forwards[i*3 + 1]
        fw3 = sorted_forwards[i*3 + 2]

        total_rating = gk['rating'] + def1['rating'] + def2['rating'] + fw1['rating'] + fw2['rating'] + fw3['rating']
        
        teams.append({
            'goalkeeper': gk,
            'defenders': [def1, def2],
            'forwards': [fw1, fw2, fw3],
            'total_rating': total_rating
        })
    
    return teams


def optimize_teams(teams, iterations=100):
    for _ in range(iterations):
        teams.sort(key=lambda x: x['total_rating'])
        
        weakest = teams[0]
        strongest = teams[-1]
        
        # Пробуем обменять случайных игроков одинаковых ролей
        role = random.choice(['defenders', 'forwards'])
        weak_player = random.choice(weakest[role])
        strong_player = random.choice(strongest[role])
        
        # Проверяем, улучшит ли это баланс
        diff = strong_player['rating'] - weak_player['rating']
        new_weak_rating = weakest['total_rating'] + diff
        new_strong_rating = strongest['total_rating'] - diff
        
        if abs(new_weak_rating - new_strong_rating) < abs(weakest['total_rating'] - strongest['total_rating']):
            weakest[role].remove(weak_player)
            weakest[role].append(strong_player)
            strongest[role].remove(strong_player)
            strongest[role].append(weak_player)
            
            # Обновляем общие рейтинги
            weakest['total_rating'] = new_weak_rating
            strongest['total_rating'] = new_strong_rating


def getMatchObject(id, team1, team2):
    match = {
        'match_id': id,
        'matchRating': round((team1['total_rating'] + team2['total_rating']) / 12),
                    
        'team1_players' : {
            'Вратарь': [{'name': team1['goalkeeper']['name'], 'rate': team1['goalkeeper']['rating']}],
            'Защитники': [{'name': d['name'], 'rate': d['rating']} for d in team1['defenders']],
            'Нападающие': [{'name': f['name'], 'rate': f['rating']} for f in team1['forwards']]
        },

        'team2_players' : {
            'Вратарь': [{'name': team2['goalkeeper']['name'], 'rate': team2['goalkeeper']['rating']}],
            'Защитники': [{'name': d['name'], 'rate': d['rating']} for d in team2['defenders']],
            'Нападающие': [{'name': f['name'], 'rate': f['rating']} for f in team2['forwards']]
        },

        'team1_score' : 0,
        'team2_score' : 0,
    }

    return match