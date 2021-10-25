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
    "student": ['Время', 'Дисциплина', 'Преподаватель', 'Кабинет'],
    "teacher": ['Время', 'Дисциплина', 'Группа', 'Кабинет'],
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
      selectDate = datepickerInstance.selectedDates,
      fullWeekCheckbox = document.getElementById('fullWeek');

  let checkFullWeekCheckbox = fullWeekCheckbox.checked;

  let dateText = '';

  selectDate = selectDate.map(item => moment(item).format('YYYY-MM-DD'));

  if (checkFullWeekCheckbox) {
    selectDate = [moment().startOf('week').format('YYYY-MM-DD'), moment().endOf('week').format('YYYY-MM-DD')];
    dateText = 'неделю'
  } else {
    dateText = moment(selectDate[0]).format('DD.MM.YYYY')
  };


  document.querySelector('.main-info').style.display = 'flex';
  document.getElementById('groupName').innerHTML = `класс: ${getSelectText()}`;
  document.getElementById('date').innerHTML = `расписание на ${dateText}`;

  let params = {selectValue, selectDate}

  axios.get('/search', {
    params
  }).then(response => {

    let data = deserialize(response.data);

    let tbody = document.getElementById('tbody');

    let html = '';

    if (!data?.length) {
      tbody.innerHTML = html;

      return false;
    }

    if (checkFullWeekCheckbox) {
      let result = [];

      let dayFormatData = Array.from(new Set(data.map(item => item.day )));

      dayFormatData.forEach((item, index) =>{
          result[index] = data.filter(subitem => subitem.day == item )
      });

      result.forEach(item => {
        item.forEach((subitem, index) => {

          if (index === 0) {
            let trDayName = `<tr> 
              <td colspan="4">${moment(subitem.day).format('DD.MM.YYYY')}</td>
            </tr>`;

            html += trDayName;
          }

          let tr = `<tr> 
              <td width="15%" align="center">${subitem.time}</td>
              <td>${subitem.discipline}</td>
              <td>${subitem.teacher__fio}</td>
              <td width="15%" align="center">${subitem.place}</td>
            </tr>`;

            html += tr;
        })
      })

    } else {
      data.forEach(item => {
        let tr = `<tr> 
          <td width="15%" align="center">${item.time}</td>
          <td>${item.discipline}</td>
          <td>${item.teacher__fio}</td>
          <td width="15%" align="center">${item.place}</td>
        </tr>`;
  
        html += tr;
      });
    }

    tbody.innerHTML = html;
  });
}

function getSelectText() {
  let select = document.getElementById('group');

  return select.options[select.selectedIndex].text;
}

function deserialize(data) {
  let formatData = JSON.parse(data)

  return formatData
}