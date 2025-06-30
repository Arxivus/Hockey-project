import { getTimetableMatches } from './fetch-requests.js'

window.onload = async function() {
    const matchesTable = document.querySelector('.timetable-matches');
    const data = await getTimetableMatches('/timetable/get-matches/')
    const matches = data['matches']

    const filterBlock = document.querySelector('.filter-groups');
    filterBlock.style.display = 'flex'

    const filterEl = document.querySelector('.filter');
    filterEl.addEventListener('change', function(e) {
        const filterValue = e.target.value;

        const filteredMatches = filterMatches(matches, filterValue) 
        renderTimetableMatches(filteredMatches, matchesTable)     
    })

    renderTimetableMatches(matches, matchesTable) 
}


function renderTimetableMatches(matches, matchesTable) {
    matchesTable.innerHTML = ''

    for (let i = 0; i < matches.length; i++) {
        const match = matches[i]
        const matchTime = match['start_time'].slice(0, 5)
        const matchField = match['field_num']
        const matchGroupId = match['group_id']
        const matchScore1 = match['team1_score']
        const matchScore2 = match['team2_score']
        const team1Block = getTeamBlock(match['team1_players'])
        const team2Block = getTeamBlock(match['team2_players'])

        const matchCard = getMatchCard(matchGroupId, matchTime, matchField, team1Block, team2Block, matchScore1, matchScore2)  
        matchesTable.append(matchCard)
    }
}

function getTeamBlock(team) {
    const teamBlock = document.createElement('div');
    teamBlock.classList.add('team-block')

    const playersBlock = document.createElement('div')
    playersBlock.classList.add('team-players')

    const teamRoles = Object.keys(team)
    for (let i = 0; i < teamRoles.length; i++) {
        const roleName = teamRoles[i]
        const rolePlayers = team[roleName];

        rolePlayers.forEach((player, index) => {
            const playerEl = document.createElement('p');
            if (i + index === teamRoles.length + rolePlayers.length - 2) {
                playerEl.textContent = player.id
            } else {
                playerEl.textContent = `${player.id},`
            }
            playersBlock.append(playerEl);
        }); 
    }
    
    teamBlock.append(playersBlock)
    return teamBlock
}

function getMatchCard(matchGroupId, matchTime, fieldNum, team1Block, team2Block,  matchScore1, matchScore2) {
    const matchCard = document.createElement('div');
    matchCard.setAttribute('data-group', matchGroupId)
    matchCard.classList.add('match-card')
    const matchInfo = document.createElement('div');
    matchInfo.classList.add('match-info')

    const time = document.createElement('span');
    time.textContent = matchTime
    const field = document.createElement('span');
    field.textContent = `Поле №${fieldNum}`
    const score = document.createElement('span');
    score.textContent = `${matchScore1}:${matchScore2}`
    matchInfo.append(time, field, score)
    
    const teamsBlock = document.createElement('div');
    teamsBlock.classList.add('teams-block')
    teamsBlock.append(team1Block, team2Block) 

    matchCard.append(matchInfo, teamsBlock)
    return matchCard
}

function filterMatches(matches, filter) {
    if (filter == 0) { return matches }

    else {
        const filtered = matches.filter(match => match['group_id'] == filter);
        return filtered
    }   
}

export {
    renderTimetableMatches
}