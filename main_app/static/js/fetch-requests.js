import { renderMatches } from './tour-elems-renders.js'
import { renderRatingsTable } from './rate-table-render.js'

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


function getMatchesData(matchesTable, url) {
    fetch(url, 
        {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => renderMatches(data['matches'], matchesTable)) 
        .catch(error => console.error('Ошибка получения данных:', error))
}

function generateMatches(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function getNextMatch(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function getGeneratedMatches(matchesTable, url) {
    getMatchesData(matchesTable, url)
}

function saveMatchScore(matchId, score1, score2) {
    fetch(`/tournaments/save-match/${matchId}/`, 
        {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ team1_score: score1, team2_score: score2 })
        })
        .then(response => response.json())
        .then(data => console.log(data['message']))
        .catch(error => console.error('Ошибка сохранения:', error))
} 

function getCompetitors() {
    fetch('/ratings/get-competitors/', 
        {
            method: 'GET',
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => renderRatingsTable(data['competitors']))
        .catch(error => console.error('Ошибка получения данных:', error))
} 

export {
    generateMatches,
    getNextMatch,
    getGeneratedMatches,
    saveMatchScore,
    getCompetitors
}