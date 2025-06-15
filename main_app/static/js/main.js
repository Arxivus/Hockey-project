import { generateTour, shiftMatchesTime, getGeneratedMatches, checkRegisterStatus } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    const matchesTable = document.querySelector('.matches');

    const generateBtn = document.querySelector('.generate-btn');
    const modalTourWindow = document.querySelector('.modal-edit');
    const closeBtn = document.querySelector('.modal-close');
    const saveTourSettingsBtn = document.querySelector('.modal-save-btn');

    const shiftTimeBtn = document.querySelector('.shift-btn');
    const modalTimeWindow = document.querySelector('.modal-time-edit');
    const closeBtn2 = document.querySelector('.modal-time-close');
    const shiftTime = document.querySelector('.modal-shift-btn');

    const overlay = document.getElementById('overlay');

    getGeneratedMatches(matchesTable, '/tournaments/get-stored-matches/')

    checkRegister('/tournaments/check-register/')
    
    generateBtn.addEventListener('click', function() {
            modalTourWindow.style.display = 'flex'
            overlay.classList.add('show')
    })

    closeBtn.addEventListener('click', () => {
        modalTourWindow.style.display = 'none'
        overlay.classList.remove('show')
    })

    saveTourSettingsBtn.addEventListener('click', (e) => {
        generateBySettings(e, modalTourWindow, overlay)       
    }) 



    shiftTimeBtn.addEventListener('click', () => {
        modalTimeWindow.style.display = 'flex'
        overlay.classList.add('show')
    })

    closeBtn2.addEventListener('click', () => {
        modalTimeWindow.style.display = 'none'
        overlay.classList.remove('show')
    })
    
    shiftTime.addEventListener('click', (e) => {
        shiftByTime(e, modalTimeWindow, overlay)
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


function generateBySettings(e, modalTourWindow, overlay) {
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
            modalTourWindow.style.display = 'none'
            overlay.classList.remove('show')
            setTimeout(function() {location.reload()}, 3000);
        }

        else {
            const error = document.querySelector('.form-error');
            error.textContent = 'Неверный формат данных!'
        }
}


function shiftByTime(e, modalTimeWindow, overlay){
    e.preventDefault()
        const shift_time = document.getElementById('matches-shift');
        
        if (shift_time.value != '') {
            console.log('aboba');
            const loading = document.querySelector('.loading');
            loading.style.display = 'flex'

            shiftMatchesTime(shift_time.value, '/tournaments/shift-matches-time/')
            modalTimeWindow.style.display = 'none'
            overlay.classList.remove('show')
            setTimeout(function() {location.reload()}, 3000);
        }

        else {
            const error = document.querySelector('.shift-form-error');
            error.textContent = 'Вы не указали время'
        }
}