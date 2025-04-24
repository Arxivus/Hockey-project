function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.querySelector('.generate-btn');
    const matchesTable = document.querySelector('.matches');

    generateBtn.addEventListener('click', function() {
        fetch('http://127.0.0.1:8000/tournaments/generate-teams/', 
        {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => renderTeams(data['teams'], matchesTable)) 
        .catch(error => console.error('Ошибка:', error))
    })
});

function renderTeams(teams, matchesTable) {
    console.log(teams);

    for (let i = 0; i < teams.length - 1; i++) {
        const team1Card = getTeamCard(teams[i], i);
        const team2Card = getTeamCard(teams[i + 1], i + 1);

        const matchRating = Math.floor((teams[i].total_rating + teams[i + 1].total_rating) / 12)
        const matchCard = getMatchCard(team1Card, team2Card, matchRating)
        matchesTable.append(matchCard)
    }
}

function getTeamCard(team, index) {
    return card = `<div class="team-card">
            <h5>Команда ${index + 1}</h5>
            <p><strong>Вратарь:</strong> ${team.goalkeeper.name}</p>
            <p><strong>Защитники:</strong> ${team.defenders.map(d => d.name).join(', ')}</p>
            <p><strong>Нападающие:</strong> ${team.forwards.map(f => f.name).join(', ')}</p>
        </div>`
}

function getMatchCard(team1Card, team2Card, matchRating) {
    const matchCard = document.createElement('div');
    matchCard.classList.add('match-card')

    const matchTeams = document.createElement('div');
    matchTeams.classList.add('match-teams')
    matchTeams.innerHTML += team1Card
    matchTeams.innerHTML += team2Card
    
    const matchTitle = document.createElement('h4');
    matchTitle.classList.add('match-title')
    matchTitle.textContent = `Микроматч / Средний рейтинг: ${matchRating}`

    matchCard.append(matchTitle, matchTeams)
    return matchCard
}