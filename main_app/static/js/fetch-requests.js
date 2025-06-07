import { renderMatches } from './tour-elems-renders.js'


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

function getPermissions(url) {
    return fetch(url, {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => data)
}


function getMatchesData(matchesTable, url) {
    fetch(url, 
        {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            if (data['message']) {
                console.log(data['message']);
            }
            renderMatches(data['matches'], matchesTable);
        }) 
        .catch(error => console.error('Ошибка получения данных:', error))
}

function generateMatches(matchesTable, url) {
    const matchesBlock = document.querySelector('.matches');
    matchesBlock.innerHTML = ''
    getMatchesData(matchesTable, url)
}

function getNextMatch(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function getGeneratedMatches(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function saveMatchScore(matchId, score1, score2, team1_playersId, team2_playersId) {
    fetch(`/tournaments/save-match/${matchId}/`, 
        {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ 
                team1_score: score1,
                team2_score: score2,
                team1_playersId: team1_playersId,
                team2_playersId: team2_playersId
            })
        })
        .then(response => response.json())
        .then(data => console.log(data['message']))
        .catch(error => console.error('Ошибка сохранения:', error))
} 

async function getCompetitors() {
    let response = await fetch('/ratings/get-competitors/', 
    {
        method: 'GET',
        headers: { 'X-CSRFToken': csrftoken }
    }).catch(error => console.error('Ошибка получения данных:', error))

    return await response.json()
} 

async function checkRegisterStatus() {
    let response = await fetch('/tournaments/check-register/', 
    {
        method: 'GET',
        headers: { 'X-CSRFToken': csrftoken }
    }).catch(error => console.error('Ошибка обращения', error))

    return await response.json()
}

export {
    generateMatches,
    getNextMatch,
    getGeneratedMatches,
    saveMatchScore,
    getCompetitors,
    getPermissions,
    checkRegisterStatus
}