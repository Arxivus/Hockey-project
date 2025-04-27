import { saveMatchScore } from './fetch-requests.js';

function renderMatches(matches, matchesTable) { 
    console.log(matches);
    for (let i = 0; i < matches.length; i++) {
        const match = matches[i]
        const matchRating = match['matchRating']
        
        const matchId = match['match_id'] 
        const team1_score = match['team1_score']
        const team2_score = match['team2_score']

        const team1Card = getTeamCard(match['team1_players'])
        const team2Card = getTeamCard(match['team2_players'])

        const matchCard = getMatchCard(team1Card, team2Card, matchRating, matchId, team1_score, team2_score)  
        matchCard.setAttribute('data-uuid', matchId) 

        matchesTable.prepend(matchCard)
    }
}

function createTeamRoleEl(roleName, rolePlayers) {
    const roleEl = document.createElement('span');
    roleEl.textContent = `${roleName}:`

    const playersBlock = document.createElement('div')
    playersBlock.classList.add('team-roles')
    playersBlock.append(roleEl)

    rolePlayers.forEach((player) => {
        const playerEl = document.createElement('p');
        playerEl.textContent = `${player.name}, ${player.rate}`
        playersBlock.append(playerEl)
    }); 
    
    return playersBlock
}

function getTeamCard(team) {
    const teamCard = document.createElement('div')
    teamCard.classList.add('team-card')
   
    const teamTitle = document.createElement('h5');
    teamTitle.textContent = 'Состав команды:'
    teamCard.append(teamTitle)
   
    const teamRoles = Object.keys(team)
    for (let i = 0; i < teamRoles.length; i++) {
        const roleName = teamRoles[i]
        const rolePlayers = team[roleName];

        const teamRoleEl = createTeamRoleEl(roleName, rolePlayers)
        teamCard.append(teamRoleEl)
    }
    
    return teamCard
}

function getMatchCard(team1Card, team2Card, matchRating, matchId, team1_score, team2_score) {
    const matchCard = document.createElement('div')
    matchCard.classList.add('match-card')

    const matchTitle = document.createElement('h4')
    matchTitle.classList.add('match-title')
    matchTitle.textContent = `Микроматч / Средний рейтинг: ${matchRating}`

    const matchTeams = document.createElement('div')
    matchTeams.classList.add('match-teams')
    matchTeams.append(team1Card, team2Card)
    
    const matchScoreEl = document.createElement('div');
    matchScoreEl.classList.add('match-score')

    const matchScoreTitle = document.createElement('h5')
    matchScoreTitle.classList.add('match-score-title')
    matchScoreTitle.textContent = 'Итоговый счет: '

    const team1Score = document.createElement('input')
    team1Score.classList.add('team1-score-input')
    team1Score.setAttribute('type', 'number')
    team1Score.value = team1_score

    const separatorEl = document.createElement('p')
    separatorEl.textContent = ':'

    const team2Score = document.createElement('input')
    team2Score.classList.add('team2-score-input')
    team2Score.setAttribute('type', 'number')
    team2Score.value = team2_score

    const saveScoreBtn = document.createElement('button')
    saveScoreBtn.classList.add('save-score-btn')
    saveScoreBtn.setAttribute('data-uuid', matchId);
    saveScoreBtn.textContent = 'Сохранить счет'

    saveScoreBtn.addEventListener('click', (event) => {
        const currentCard = event.currentTarget.closest('.match-card')
        const score1 = currentCard.querySelector('.team1-score-input').value
        const score2 = currentCard.querySelector('.team2-score-input').value
        
        saveMatchScore(matchId, score1, score2);
    })
   
    matchScoreEl.append(matchScoreTitle, team1Score, separatorEl, team2Score, saveScoreBtn)

    matchCard.append(matchTitle, matchTeams, matchScoreEl)
    return matchCard
}

export {
    renderMatches
}