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

function getGeneratedMatches(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function getNextMatch(matchesTable, url) {
    getMatchesData(matchesTable, url)
}
/* function getNextMatch(matchesTable, groupId, url) {
    fetch(url, 
        {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ group_id: groupId })
        })
        .then(response => response.json())
        .then(data => {
            if (data['message']) {
                console.log(data['message']);
            }
            renderMatches(data['matches'], matchesTable);
        }) 
        .catch(error => console.error('Ошибка получения данных:', error))
} */


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

async function getTimetableMatches(url) { 
    return await getData(url)
}

async function getCompetitors(url) { 
    return await getData(url)
}

async function checkRegisterStatus(url) { 
    return await getData(url)
}

async function getData(url) {
    let response = await fetch(url, 
    {
        method: 'GET',
        headers: { 'X-CSRFToken': csrftoken }
    }).catch(error => console.error('Ошибка получения данных:', error))

    return await response.json()
} 



function saveProfileChanges(newValues) {
    fetch('/user/edit-profile/', 
    {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({newValues})
    })
    .then(response => response.json())
    .then(data => console.log(data['message']))
    .catch(error => console.error('Ошибка сохранения:', error))
} 

function generateTour(tourSettings, url) {
    fetch(url, 
    {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({tourSettings})
    })
    .then(response => response.json())
    .then(data => console.log(data['message']))
    .catch(error => console.error('Ошибка создания:', error))
} 

export {
    generateTour,
    /* generateMatches, */
    getNextMatch,
    getGeneratedMatches,
    saveMatchScore,
    getCompetitors,
    getPermissions,
    checkRegisterStatus,
    saveProfileChanges,
    getTimetableMatches
}