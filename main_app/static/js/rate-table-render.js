import { getCompetitors } from './fetch-requests.js'

document.addEventListener('DOMContentLoaded', function() {
    getCompetitors()
});

function renderRatingsTable(competitors) {
    const rateTable = document.querySelector('.table-rows');
    const tableHeaders = document.createElement('table');
    tableHeaders.classList.add('table-headers')

    const ratingsBlock = document.querySelector('.ratings-block');

    const rateTableHeaders = createTableRow('№', 'ФИО', 'Возраст', 'Рейтинг')
    tableHeaders.append(rateTableHeaders)

    ratingsBlock.prepend(tableHeaders)

    for (let i = 0; i < competitors.length; i++) {
        const competitor = competitors[i];
        const row = createTableRow(i+1, competitor['fullname'], competitor['age'], competitor['rating'])

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

export {
    renderRatingsTable
}