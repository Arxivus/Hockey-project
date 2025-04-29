import { generateMatches, getGeneratedMatches } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.querySelector('.generate-btn');
    const matchesTable = document.querySelector('.matches');

    getGeneratedMatches(matchesTable)

    generateBtn.addEventListener('click', function() {
        generateMatches(matchesTable)
    })
});