import { getCompetitors } from './fetch-requests.js'

window.onload = async function() {
    const data = await getCompetitors()
    let competitors = data['competitors']
    const tableHeadersBlock = document.querySelector('.table-headers-block');
    const tableHeaders = document.createElement('table');
    tableHeaders.classList.add('table-headers')

    const rateTableHeaders = createTableRow('№', 'ФИО', 'Возраст', 'Пол', 'Рейтинг')
    tableHeaders.append(rateTableHeaders)
    tableHeadersBlock.append(tableHeaders)
    
    const filterEl = document.querySelector('.filter');
    filterEl.addEventListener('change', function(e) {
        const filterValue = e.target.value;
        console.log(filterValue);
        competitors = sortByFilter(competitors, filterValue) 
        renderRatingsTable(competitors)     
    })

    renderRatingsTable(competitors)
};

function renderRatingsTable(competitors) {
    const rateTable = document.querySelector('.table-rows');
    rateTable.innerHTML = ''

    for (let i = 0; i < competitors.length; i++) {
        const competitor = competitors[i];
        const genderLetter = competitor['gender'] === 'M' ? 'М' : 'Ж'
        const row = createTableRow(i+1, competitor['name'], competitor['age'], genderLetter, competitor['rating'])

        rateTable.append(row)
    }
}

function createTableRow() {
    const tableRow = document.createElement('tr');

    for (let i = 0; i < arguments.length; i++) {
        const value = arguments[i];
        const tableData = document.createElement('td'); 
        tableData.textContent = value
        tableRow.append(tableData)
    }
    return tableRow
}

function sortByFilter(players, filter) {
    switch (filter) {
        case 'age': 
            players.sort((a, b) => a.age - b.age);
            break
            
        case '-age': 
            players.sort((a, b) => b.age - a.age)
            break

        case '-rating': 
            players.sort((a, b) => { return b.rating - a.rating })
            break

        case 'M': 
            players.sort((a, b) => a.gender.localeCompare(b.gender))
            break

        case 'W': 
            players.sort((a, b) => b.gender.localeCompare(a.gender));
            break
    }
    return players
  
}

export {
    renderRatingsTable
}