import { getTimetableMatches } from './fetch-requests.js'

window.onload = async function() {
    const data = await getTimetableMatches('/timetable/get-matches/')
    const matches = data['matches']

    const filterBlock = document.querySelector('.filter-groups');
    filterBlock.style.display = 'flex'

    const filterEl = document.querySelector('.filter');
    filterEl.addEventListener('change', function(e) {
        const filterValue = e.target.value;

        const filteredMatches = filterMatches(matches, filterValue) 
        renderTimetableMatches(filteredMatches)     
    })

    renderTimetableMatches(matches) 
}


function renderTimetableMatches(matches) {
    const matchesTable = document.querySelector('.timetable-matches');
    matchesTable.innerHTML = ''

    for (let i = 0; i < matches.length; i++) {
        const match = matches[i]
        const matchTime = match['start_time'].slice(0, 5)
        const matchField = match['field_num']
        const matchGroupId = match['group_id']
        const team1Block = getTeamBlock(match['team1_players'], 1)
        const team2Block = getTeamBlock(match['team2_players'], 2)

        const matchCard = getMatchCard(matchGroupId, matchTime, matchField, team1Block, team2Block)  
        matchesTable.append(matchCard)
    }
}

function getTeamBlock(team, teamNum) {
    const teamBlock = document.createElement('div');
    teamBlock.classList.add('team-block')
    const teamTitle = document.createElement('h5');
    teamTitle.textContent = `Команда ${teamNum}`

    const playersBlock = document.createElement('div')
    playersBlock.classList.add('team-players')

    const teamRoles = Object.keys(team)
    for (let i = 0; i < teamRoles.length; i++) {
        const roleName = teamRoles[i]
        const rolePlayers = team[roleName];

        rolePlayers.forEach((player) => {
            const playerEl = document.createElement('p');
            playerEl.textContent = `${player.name}`
            playersBlock.append(playerEl)
        }); 
    }
    
    teamBlock.append(teamTitle, playersBlock)
    return teamBlock
}

function getMatchCard(matchGroupId, matchTime, fieldNum, team1Block, team2Block) {
    const matchCard = document.createElement('div');
    matchCard.setAttribute('data-group', matchGroupId)
    matchCard.classList.add('match-card')
    const matchInfo = document.createElement('div');
    matchInfo.classList.add('match-info')

    const time = document.createElement('span');
    time.textContent = matchTime
    const field = document.createElement('span');
    field.textContent = `Поле №${fieldNum}`
    matchInfo.append(time, field)

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