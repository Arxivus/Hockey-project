import { saveMatchScore } from './fetch-requests.js';

function renderMatches(matches, matchesTable) {
    if (matches === undefined) {
        console.log('Nothing to render');
        return
    } 

    for (let i = 0; i < matches.length; i++) {
        const match = matches[i]
        const matchRating = match['matchRating']
        const matchId = match['match_id'] 
        const team1Card = getTeamCard(match['team1_players'], match['team1_score'], 1)
        const team2Card = getTeamCard(match['team2_players'], match['team2_score'], 2)

        const team1_playersId = getTeamPlayersId(match['team1_players'])
        const team2_playersId = getTeamPlayersId(match['team2_players'])

        const matchCard = getMatchCard(team1Card, team2Card, matchRating, matchId, team1_playersId, team2_playersId)  
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

function getTeamCard(team, team_score, num) {
    const teamCard = document.createElement('div')
    teamCard.classList.add('team-card')

    const teamScore = document.createElement('input')
    teamScore.classList.add(`team${num}-score-input`)
    teamScore.setAttribute('type', 'number')
    teamScore.value = team_score
   
    const teamTitle = document.createElement('h5');
    teamTitle.textContent = 'Состав команды'
    teamCard.append(teamScore, teamTitle)

    const teamPlayersBlock = document.createElement('div');
    teamPlayersBlock.classList.add('team-players-block')
    
    const teamRoles = Object.keys(team)
    for (let i = 0; i < teamRoles.length; i++) {
        const roleName = teamRoles[i]
        const rolePlayers = team[roleName];

        const teamRoleEl = createTeamRoleEl(roleName, rolePlayers)
        teamPlayersBlock.append(teamRoleEl)
    }
    
    teamCard.append(teamPlayersBlock)
    return teamCard
}

function getMatchCard(team1Card, team2Card, matchRating, matchId, team1_playersId, team2_playersId) {
    const matchCard = document.createElement('div')
    matchCard.classList.add('match-card')

    const matchTitle = document.createElement('h4')
    matchTitle.classList.add('match-title')
    matchTitle.textContent = `Матч / Средний рейтинг: ${matchRating}`

    const matchPlaceBlock = document.createElement('div')
    matchPlaceBlock.classList.add('match-place')
    const matchPlace = document.createElement('h4'); 
    matchPlace.textContent = '12:00 / Поле №'
    matchPlaceBlock.append(matchTitle, matchPlace)

    const matchSaveBlock = document.createElement('div');
    matchSaveBlock.classList.add('match-save')

    const VS = document.createElement('img');
    VS.classList.add('vs-img')
    VS.setAttribute('src', '/static/images/vs.png')

    const saveScoreBtn = document.createElement('button')
    saveScoreBtn.classList.add('save-score-btn')
    saveScoreBtn.setAttribute('data-uuid', matchId);
    saveScoreBtn.textContent = 'Сохранить счет'
    saveScoreBtn.addEventListener('click', (event) => {
        const currentCard = event.currentTarget.closest('.match-card')
        const score1 = currentCard.querySelector('.team1-score-input').value
        const score2 = currentCard.querySelector('.team2-score-input').value
        saveMatchScore(matchId, score1, score2, team1_playersId, team2_playersId);
    })

    matchSaveBlock.append(VS, saveScoreBtn)

    const matchTeams = document.createElement('div')
    matchTeams.classList.add('match-teams')
    matchTeams.append(team1Card, matchSaveBlock, team2Card)

    matchCard.append(matchPlaceBlock, matchTeams)
    return matchCard
}

function getTeamPlayersId(team) {
    const players_id = []
    const teamRoles = Object.keys(team)

    for (let i = 0; i < teamRoles.length; i++) {
        const teamRole = teamRoles[i]
        const rolePlayers = team[teamRole]

        rolePlayers.forEach((player) => {
            players_id.push(player.id)
        });   
    }

    return players_id
}

export {
    renderMatches
}