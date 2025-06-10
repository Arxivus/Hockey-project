from .models import Competitor, Profile
import numpy as np

# протестировать изменение рейтингов
# добавить pool 

def updatMatchPlayersScore(diff_score1, diff_score2, team1_playersId, team2_playersId): 
    all_match_id = list(team1_playersId) + list(team2_playersId)

    for id in all_match_id:
        player = Competitor.objects.get(player_id=id)

        if id in team1_playersId:
            player.goals_scored += diff_score1
            player.goals_taken += diff_score2

        else:
            player.goals_scored += diff_score2 
            player.goals_taken += diff_score1

        player.save()

# -------------------------------------------------------------------------------------------

def changeRatingValue(players_pool_id, match_players_id, new_ratings):
    for i in range(len(new_ratings)):
        id = players_pool_id[i]
        if id in match_players_id:
            player = Competitor.objects.get(player_id=id)
            player.rating = new_ratings[i]
            player.save()
            if player.profile is not None:
                player.profile.rating = new_ratings[i]
                prev_ratings = player.profile.previous_ratings
              
                if len(prev_ratings) >= 10:
                    prev_ratings.pop(0)
                prev_ratings.append(new_ratings[i])
                player.profile.previous_ratings = prev_ratings

                player.profile.save()


def getNewRatings(A, B, pl_count, players_pool_id):
    lambda_reg = 1                              # параметр регуляризации
    current_ratings = np.array([Competitor.objects.get(player_id=id).rating for id in players_pool_id])
    A_reg = np.identity(pl_count) * lambda_reg  # добавляем lambda * ||x||^2
    B_reg = current_ratings * lambda_reg        # обеспечение небольшого разброса с прошлым рейтингом

    A_full = np.vstack([A, A_reg])              # объединение
    B_full = np.hstack([B, B_reg])

    return np.linalg.lstsq(A_full, B_full, rcond=None)[0]


def getSumRatings(players_pool):
    avg_rating = 0
    for id in players_pool:
        avg_rating += Competitor.objects.get(player_id=id).rating
    return avg_rating


def addEquationInSystem(matches_played_matrix, player, match_players_id, A_matrix, B_matrix, pos, players_pool):
    delta_coeff = 200
    scored = player.goals_scored
    taken = player.goals_taken
    if scored + taken == 0 or player.matches_played == 0:
        return

    delta = delta_coeff * (scored - taken) / (scored + taken) # правая часть уравнения

    pl_in_team = len(match_players_id)/2
    i = 0
    for id in players_pool:
        matches_with = matches_played_matrix[player.player_id][id][0] 
        matches_against = matches_played_matrix[player.player_id][id][1]
        coeff = 1 / (player.matches_played * pl_in_team)

        A_matrix[pos][i] = coeff * matches_with - coeff * matches_against
        i += 1
    B_matrix[pos] = delta


def updateRatings(tournament, team1_playersId, team2_playersId):
    matches_played_matrix = tournament.played_with_matrix

    group_id = Competitor.objects.get(player_id=team1_playersId[0]).group_id
    players_pool_id = list(Competitor.objects.filter(group_id=group_id).values_list('player_id', flat=True)) # пул id игроков матча

    pl_count = len(players_pool_id)
    match_players_id = list(team1_playersId) + list(team2_playersId)

    coeff_matrix = [ [0 for _  in range(pl_count)] for _ in range(pl_count + 1) ] # коэффициенты сокомандников и противников
    res_matrix = [0 for _ in range(pl_count + 1)]                                 # правая часть - delta каждого

    pos = 0
    for id in players_pool_id:
        player = Competitor.objects.get(player_id=id)
        # + уравнение рейтинга для каждого игрока в матрицу
        addEquationInSystem(matches_played_matrix, player, match_players_id, coeff_matrix, res_matrix, pos, players_pool_id) 
        pos += 1

    coeff_matrix[pl_count] = [1 for _ in range(pl_count)] # добавление уравнения баланса рейтинга в матче
    res_matrix[pl_count] = getSumRatings(players_pool_id)

    new_ratings = getNewRatings(coeff_matrix, res_matrix, pl_count, players_pool_id) # новые рейтинги всех игроков матча
    rounded_ratings = [round(i) for i in new_ratings]

    changeRatingValue(players_pool_id, match_players_id, rounded_ratings)
