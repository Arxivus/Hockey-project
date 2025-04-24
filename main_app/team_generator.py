import random

def generate_teams(players):
    forwards, defenders, goalkeepers  = [], [], []

    for pl in players:
        match pl['role']:
            case '1': forwards.append(pl)
            case '2': defenders.append(pl)
            case '3': goalkeepers.append(pl)
    
    teams = balance_teams(forwards, defenders, goalkeepers)
    optimize_teams(teams)
    return teams


def balance_teams(forwards, defenders, goalkeepers):
    num_teams = min(len(goalkeepers), len(defenders)//2, len(forwards)//3)
    teams = []
    
    # Сортируем игроков по рейтингу (лучшие сначала)
    sorted_forwards = sorted(forwards, key=lambda x: -x['rating'])
    sorted_defenders = sorted(defenders, key=lambda x: -x['rating'])
    sorted_goalkeepers = sorted(goalkeepers, key=lambda x: -x['rating'])
  
    for i in range(num_teams):
        # Берем вратаря
        gk = sorted_goalkeepers[i]
        
        # Берем защитников 
        def1 = sorted_defenders[i*2]
        def2 = sorted_defenders[i*2 + 1]
        
        # Берем нападающих 
        fw1 = sorted_forwards[i*3]
        fw2 = sorted_forwards[i*3 + 1]
        fw3 = sorted_forwards[i*3 + 2]
        
        # Рассчитываем общий рейтинг команды
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
        # Сортируем команды по общему рейтингу
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
            # Производим обмен
            weakest[role].remove(weak_player)
            weakest[role].append(strong_player)
            strongest[role].remove(strong_player)
            strongest[role].append(weak_player)
            
            # Обновляем общие рейтинги
            weakest['total_rating'] = new_weak_rating
            strongest['total_rating'] = new_strong_rating

