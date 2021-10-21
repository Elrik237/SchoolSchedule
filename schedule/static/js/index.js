//-- Переменные --//
let datepickerInstance = null;

//-- /Переменные --//


//-- Слушатели --//
document.addEventListener("DOMContentLoaded", readyDocument);
document.getElementById('searchForm').addEventListener("submit", submitSearchForm);
//-- /Слушатели --//


// Заголовки таблицы в зависимости от типа расписания (для студентов, преподователей и т.д.)
function getTableHeader(type) {
  const table_headers = {
    "student": ['Время', 'Дисциплина', 'Преподаватель', 'Ауд/Адрес'],
    "teacher": ['Время', 'Дисциплина', 'Группа', 'Ауд/Адрес'],
  }

  return table_headers[type];
}

// Вызов функций при загрузке документа
function readyDocument() {
  initDatepicker();
  initTable();
}

// Инициализация календаря
function initDatepicker() {
  datepickerInstance = new AirDatepicker('#datepicker');
}

// Инициализация таблицы
function initTable(type = "student") {
  let block = document.getElementById('thead');

  let html = "";

  let headers = getTableHeader(type);

  headers.forEach(item => {
    html += `<th>${item}</th>`;
  });

  block.innerHTML = html;
}

// Показать расписание
function submitSearchForm(event) {
  event.preventDefault();
  
  let selectValue = document.getElementById('group').value,
      selectDate = datepickerInstance.viewDate,
      fullWeekCheckbox = document.getElementById('fullWeek');

  if (fullWeekCheckbox.checked) {
    
  };

  let params = {selectValue, selectDate}

  axios.get('/search', {
    params
  }).then(response => {
    let tbody = document.getElementById('tbody');

    let html = '';

    if (response.data.length === 0) {
      return
    }

    response.data.forEach(item => {
      let tr = `<tr> 
        <td>${item.time}</td>
        <td>${item.discipline}</td>
        <td>${item.name}</td>
        <td>${item.place}</td>
      </tr>`;

      html += tr;
    });

    tbody.innerHTML = html;
  });

}