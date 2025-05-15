    # ввод счета +
    # после нажатия кнопки "сохранить" отправить POST-запрос матчем, id игроков по командам +
    # учесть обновление счета (изменение с 1 на 3, например, при увеличении счетчика +
    # далее обновить матрицу ([i][j] - кол-во забитых голов i команде с j) +
    # обновить поля игроков со счетом, вызвать функцию обновления рейтинга:
    #   составить ур-я в матричном виде: AX = B (нужны id игроков в первой и второй команде, счет текущий, матрица голов)
    #   проверить на !=0 коэффициенты
    #   в функции решить систему, получив новые рейтинги для каждого игрока
    #   присвоить полученные рейтинги по id

    # нажатие кнопки генерации еще одного матча



def updateGoalsMatrix(tournament, diff_score1, diff_score2, team1_playersId, team2_playersId):

    matrix = tournament.goal_matrix

    for current_id in team1_playersId:
        for another_id in team1_playersId:
            if current_id == another_id:
                continue
            matrix[current_id][another_id] += diff_score1

    for current_id in team2_playersId:
        for another_id in team2_playersId:
            if current_id == another_id:
                continue
            matrix[current_id][another_id] += diff_score2
    
    tournament.goal_matrix = matrix
    tournament.save()  

# после решения системы рейтинги нужно обновить
# обновлять у уже полученных объектов или отправлять в бд и получать их каждый раз из бд 
# если второй вариант, то (у модели игрока поля: З и П, кол-во сыгранных) получать значения полей из бд 
# генерация систем уравнений отдельной функцией - все равно обращаться к бд по id, 



def updateRatings(tournament, team1_playersId, team2_playersId):
    print()
