//-- Переменные --//
let datepickerInstance = null,
    type = 'group';
//-- /Переменные --//


// -- Вспомогательные функции -- //
const getLength = arr => arr.flat(Infinity).length;
// -- .Вспомогательные функции -- //


//-- Слушатели --//
document.addEventListener("DOMContentLoaded", readyDocument);
document.getElementById('searchForm').addEventListener("submit", submitSearchForm);
document.getElementById('showForTeacher').addEventListener('click', showForTeacher);
document.getElementById('showForGroup').addEventListener('click', showForGroup);
//-- /Слушатели --//


// Заголовки таблицы в зависимости от типа расписания (для студентов, преподователей и т.д.)
function getTableHeader() {
  const table_headers = {
    "group": ['Дата', 'Время', 'Дисциплина', 'Преподаватель', 'Кабинет'],
    "teacher": ['Дата', 'Время', 'Дисциплина', 'Класс', 'Кабинет'],
  }

  return table_headers[type];
}

// Вызов функций при загрузке документа
function readyDocument() {
  initDatepicker();
  initTable();

  datepickerInstance.selectDate(new Date());
}

// Инициализация календаря
function initDatepicker() {
  datepickerInstance = new AirDatepicker('#datepicker');
}

// Инициализация таблицы
function initTable() {
  let block = document.getElementById('thead');

  let html = "";

  let headers = getTableHeader(type);

  headers.forEach(item => {
    html += `<th>${item}</th>`;
  });

  block.innerHTML = html;
}

// Очистка таблицы
function clearTable() {
  document.getElementById('tbody').innerHTML = '';
}

// Показать расписание
function submitSearchForm(event) {
  event.preventDefault();

  let selectGroup = document.getElementById('group').value,
    selectTeacher = document.getElementById('teacher').value,
    selectDate = datepickerInstance.selectedDates,
    fullWeekCheckbox = document.getElementById('fullWeek');

  let checkFullWeekCheckbox = fullWeekCheckbox.checked;

  let dateText = '';

  selectDate = selectDate.map(item => moment(item).format('YYYY-MM-DD'));

  if (checkFullWeekCheckbox) {
    selectDate = [moment().startOf('week').format('YYYY-MM-DD'), moment().endOf('week').format('YYYY-MM-DD')];
    dateText = `${moment(selectDate[0]).format('DD.MM.YYYY')} - ${moment(selectDate[1]).format('DD.MM.YYYY')}`
  } else {
    dateText = moment(selectDate[0]).format('DD.MM.YYYY')
  };


  document.querySelector('.main-info').style.display = 'flex';
  document.getElementById('groupName').innerHTML = `класс: ${getSelectText()}`;
  document.getElementById('date').innerHTML = `${dateText}`;

  let params = { selectGroup, selectTeacher, selectDate, type }

  axios.get('/search', {
    params
  }).then(response => {

    if (response.data.length != 0) {
      let data = deserialize(response.data);
      showData(data, checkFullWeekCheckbox);
    } else {
      return;
    }

  });
}

// Формирование таблицы для классов
function showData(data, check) {

  const tbody = document.getElementById('tbody');

  let html = '';

  if (!data?.length) {
    tbody.innerHTML = html;

    return false;
  }

  data.forEach((day) => {
    day.forEach((item, index) => {
      let subHtml = '';

      item.forEach((subitem, subindex) => {
        let columnGroupOrTeacher = '';

        let tr;

        // Если поиск по классам, то в 4 колонку выводим имя преподавателя
        // если по преподавателям - то класс
        if (type === 'group') {
          columnGroupOrTeacher = subitem.teacher__fio;
        } else {
          columnGroupOrTeacher = subitem.group__name;
        }

        // Формирование первой колонки с датой
        let dayColumn = '';
        if (index == 0 && subindex == 0) {
          dayColumn = `<td width="15%" rowspan="${getLength(day)}" align="center">${subitem.day}</td>`
        }

        // Если урок по подгруппам
        if (item.length > 1) {

          // Формирование первой колонки с временем урока
          let timeColumn = '';
          if (subindex == 0) {
            timeColumn = `<td width="15%" rowspan="${item.length}" align="center">${subitem.time}</td>`
          }

          tr = `<tr> 
            ${dayColumn}
            ${timeColumn}
            <td>${subitem.discipline}</td>
            <td>${columnGroupOrTeacher}</td>
            <td width="15%" align="center">${subitem.place}</td>
          </tr>`
        } else {
          tr = `<tr> 
            ${dayColumn}
            <td width="15%" align="center">${subitem.time}</td>
            <td>${subitem.discipline}</td>
            <td>${columnGroupOrTeacher}</td>
            <td width="15%" align="center">${subitem.place}</td>
          </tr>`
        }

        subHtml += tr;
      })

      html += subHtml;
    })
  });

  tbody.innerHTML = html;
}

// Тест выбранного значения селекта
function getSelectText() {
  let select;

  if (type === 'group') select = document.getElementById('group');
  if (type === 'teacher') select = document.getElementById('teacher');

  return select.options[select.selectedIndex].text;
}

// Десериализация пришедсшего с бэка json
function deserialize(data) {
  let formatData = JSON.parse(data)

  return formatData
}

// Показать расписание для преподавателя
function showForTeacher() {
  document.getElementById('groupWrapper').classList.add('hide');
  document.getElementById('showForTeacher').classList.add('hide');
  document.getElementById('teacherWrapper').classList.remove('hide');
  document.getElementById('showForGroup').classList.remove('hide');

  type = 'teacher';

  initTable();
  clearTable();
}

// Показать расписание для класса
function showForGroup() {
  document.getElementById('groupWrapper').classList.remove('hide');
  document.getElementById('showForTeacher').classList.remove('hide');
  document.getElementById('teacherWrapper').classList.add('hide');
  document.getElementById('showForGroup').classList.add('hide');

  type = 'group';

  initTable();
  clearTable();
}