import { generateTour, getGeneratedMatches, checkRegisterStatus } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.querySelector('.generate-btn');
    const matchesTable = document.querySelector('.matches');
    const modalWindow = document.querySelector('.modal-edit');
    const closeBtn = document.querySelector('.modal-close');
    const saveTourSettingsBtn = document.querySelector('.modal-save-btn');

    getGeneratedMatches(matchesTable, '/tournaments/get-stored-matches/')

    checkRegister('/tournaments/check-register/')
    
    generateBtn.addEventListener('click', function() {
            modalWindow.style.display = 'flex'
            overlay.classList.add('show')
    })

    closeBtn.addEventListener('click', () => {
        modalWindow.style.display = 'none'
        overlay.classList.remove('show')
    })

    saveTourSettingsBtn.addEventListener('click', (e) => {
        e.preventDefault()
        const startTime = document.getElementById('start-time');
        const groupDelay = document.getElementById('group-delay');
        const matchDelay = document.getElementById('match-delay');
        const checkboxes = document.querySelectorAll('.multiselect-checkbox input[type="checkbox"]');
        const selectedValues = [];

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) { selectedValues.push(Number(checkbox.value)) }});

        if ( startTime.value != '' && startTime.checkValidity() && groupDelay.checkValidity() && matchDelay.checkValidity() && selectedValues.length != 0) {
            const tourSettings = [startTime.value, selectedValues, groupDelay.value, matchDelay.value]
            const loading = document.querySelector('.loading');
            loading.style.display = 'flex'

            generateTour(tourSettings, '/tournaments/start-new/')
            modalWindow.style.display = 'none'
            overlay.classList.remove('show')
            setTimeout(function() {location.reload()}, 3000);

        }

        else {
            const error = document.querySelector('.form-error');
            error.textContent = 'Неверный формат данных!'
        }       
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