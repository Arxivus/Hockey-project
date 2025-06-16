import { saveProfileChanges, getCompetitorMatches } from './fetch-requests.js'
import { renderTimetableMatches } from './timetable.js'

window.onload = async () => {
    const editProfile = document.querySelector('.profile-edit');
    const closeBtn = document.querySelector('.modal-close');
    const saveBtn = document.querySelector('.modal-save-btn');
    const modalWindow = document.querySelector('.modal-edit');
    const overlay = document.getElementById('overlay')

    const matchesTable = document.querySelector('.timetable-matches');

    if (matchesTable) {
        const user_id = document.querySelector('.user-avatar').dataset.userId;
        const data = await getCompetitorMatches(`/user/get-matches/${user_id}`)
        console.log(data['matches']);
        renderTimetableMatches(data['matches'], matchesTable)
    }
    


    if (editProfile) {
        editProfile.addEventListener('click', () => {
            modalWindow.style.display = 'flex'
            overlay.classList.add('show')
        })
    }

    closeBtn.addEventListener('click', () => {
        modalWindow.style.display = 'none'
        overlay.classList.remove('show')
    })

    saveBtn.addEventListener('click', (e) => {
        e.preventDefault()
        const newRole = document.getElementById('role')
        const newEmail = document.getElementById('email')
        const newPhone = document.getElementById('phone')
        const newAge = document.getElementById('age')
        const newCategory = document.getElementById('category')

        if (newEmail.checkValidity() && newPhone.checkValidity() && newAge.checkValidity()) {
            const newValues = [newRole.value, newEmail.value, newPhone.value, newAge.value, newCategory.value]
            saveProfileChanges(newValues)
            setTimeout(function() {location.reload()}, 500);
        }

        else {
            console.log(newEmail.checkValidity(),newPhone.checkValidity(),  newAge.checkValidity());
            const error = document.querySelector('.form-error');
            error.textContent = 'Неверный формат данных!'
        }
            
    })
}