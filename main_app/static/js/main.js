import { generateMatches, getNextMatch, getGeneratedMatches, checkRegisterStatus } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.querySelector('.generate-btn');
    const getNextMatchBtn = document.querySelector('.next-match-btn');
    const matchesTable = document.querySelector('.matches');

    getGeneratedMatches(matchesTable, '/tournaments/get-stored-matches/')

    checkRegister()
    
    generateBtn.addEventListener('click', function() {
        generateMatches(matchesTable, '/tournaments/start-new/')
    })

    getNextMatchBtn.addEventListener('click', function() {
        getNextMatch(matchesTable, '/tournaments/get-next-match/')
    })
});

async function checkRegister(){
    const isRegistered = await checkRegisterStatus()
    if (isRegistered['value']) {
        const registerBtn = document.querySelector('.register-btn');
        registerBtn.style.display = 'none'
        const registerTitle = document.querySelector('.register-title');
        registerTitle.textContent = 'Вы зарегистрированы на турнир!'
        registerTitle.style.margin = 0
    }
}