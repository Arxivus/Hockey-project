import { generateMatches, getNextMatch, getGeneratedMatches } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.querySelector('.generate-btn');
    const getNextMatchBtn = document.querySelector('.next-match-btn');
    const matchesTable = document.querySelector('.matches');

    getGeneratedMatches(matchesTable, '/tournaments/get-stored-matches/')

    generateBtn.addEventListener('click', function() {
        generateMatches(matchesTable, '/tournaments/start-new/')
    })

    getNextMatchBtn.addEventListener('click', function() {
        getNextMatch(matchesTable, '/tournaments/get-next-match/')
    })
});