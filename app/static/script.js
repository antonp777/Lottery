//Переменные
const url_api = 'http://localhost:8000/api/'

// ФУНКЦИИ

const btnDelete = document.getElementById('btn-delete')

const lotteryDeleteModal = document.getElementById('deleteLottery')
const formDeleteLottery = document.getElementById('formDeleteLottery') // Форма Delete Lottery


// Открытие модального окна Delete User
lotteryDeleteModal.addEventListener('show.bs.modal', openLotteryDeleteModal)
function openLotteryDeleteModal(event) {
    // Кнопка, которая активировала модальное окно
    const button = event.relatedTarget

    // Извлекает информацию из атрибутов data-bs-*
    const id = button.getAttribute('data-bs-whatever')
    console.log(button)
    inputDeleteId.value = id
    const urlDelete = url_api+'lottery/' + id
    fetch(urlDelete,{method: 'DELETE'})
}

// Нажатие кнопки отправки на форме Delete User
    function submitFormDeleteLotteryHandler() {
        const urlDelete = url_api + 'lottery/' + inputDeleteId.value
        fetch(urlDelete, {method: 'DELETE'})
        console.log(urlDelete)
    }

const inputDeleteId = formDeleteLottery.querySelector('#idDelete') // Input id

    formDeleteLottery.addEventListener('submit', openLotteryDeleteModal)
//
    TableLottery()

const tableLottery = document.getElementById('content_table')
tableLottery.addEventListener("submit", submitFormDeleteLotteryHandler)




// Создание таблицы Лотерей
    function TableLottery() {

        const url = url_api + 'lottery'
        const content = document.querySelector('#content_table')

        //Создание таблицы
        const table = document.createElement('table')
        table.className = "table table-hover table-light"
        content.append(table)

        // Создание заголовка таблицы
        const table_head = document.createElement('thead')
        table.append(table_head)
        const row_head = document.createElement('tr')
        row_head.className = "text-center"
        table_head.append(row_head)
        row_head.insertAdjacentHTML('beforeend', `<th>id</th>`)
        row_head.insertAdjacentHTML('beforeend', `<th>Название</th>`)
        row_head.insertAdjacentHTML('beforeend', `<th>Количество билетов</th>`)
        row_head.insertAdjacentHTML('beforeend', `<th>Цена билета</th>`)
        row_head.insertAdjacentHTML('beforeend', `<th>Статус</th>`)
        row_head.insertAdjacentHTML('beforeend', `<th>Действия</th>`)

        const table_body = document.createElement('tbody')
        table.append(table_body)


        fetch('http://localhost:8000/api/lottery')
            .then(res => {
                return res.json()
            })
            .then(data => {
                data.findIndex(
                    function (lottery) {


                        // Добавление строк с данными
                        const row = document.createElement('tr')
                        row.className = 'border-bottom border-white text-center'
                        table_body.append(row)

                        row.insertAdjacentHTML('beforeend', `<td>${lottery.id}</td>`)
                        row.insertAdjacentHTML('beforeend', `<td>${lottery.name}</td>`)
                        row.insertAdjacentHTML('beforeend', `<td>${lottery.number_tickets}</td>`)
                        row.insertAdjacentHTML('beforeend', `<td>${lottery.price_ticket}</td>`)
                        row.insertAdjacentHTML('beforeend', `<td>${lottery.status}</td>`)

                        row.insertAdjacentHTML('beforeend', `<td><button type="submit" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editLottery" data-bs-whatever="${lottery.id}" id="btnEdit">Изменить</button></td>`)
                        row.insertAdjacentHTML('beforeend', `<td><button type="submit" class="btn btn-danger" data-bs-whatever="${lottery.id}" id="btn-delete">Удалить</button></td>`)
                        //row.insertAdjacentHTML('beforeend', `<td><button type="button" class="btn btn-danger" data-bs-whatever="${lottery.id}" id="btn-delete">Удалить</button></td>`)

                    })
            })
    }

