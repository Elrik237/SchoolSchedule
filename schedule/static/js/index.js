//-- Переменные --//
let datepickerInstance = null,
    type = 'group';

//-- /Переменные --//


//-- Слушатели --//
document.addEventListener("DOMContentLoaded", readyDocument);
document.getElementById('searchForm').addEventListener("submit", submitSearchForm);
document.getElementById('showForTeacher').addEventListener('click', showForTeacher);
document.getElementById('showForGroup').addEventListener('click', showForGroup);
//-- /Слушатели --//


// Заголовки таблицы в зависимости от типа расписания (для студентов, преподователей и т.д.)
function getTableHeader() {
  const table_headers = {
    "group": ['Время', 'Дисциплина', 'Преподаватель', 'Кабинет'],
    "teacher": ['Время', 'Дисциплина', 'Класс', 'Кабинет'],
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

  let params = {selectGroup, selectTeacher, selectDate, type}

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
  let tbody = document.getElementById('tbody');

  let html = '';

  if (!data?.length) {
    tbody.innerHTML = html;

    return false;
  }

  if (check) {
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

        let columnGroupOrTeacher = '';

        if (type === 'group') {
          columnGroupOrTeacher = subitem.teacher__fio;
        } else {
          columnGroupOrTeacher = subitem.group__name;
        }

        let tr = `<tr> 
            <td width="15%" align="center">${subitem.time}</td>
            <td>${subitem.discipline}</td>
            <td>${columnGroupOrTeacher}</td>
            <td width="15%" align="center">${subitem.place}</td>
          </tr>`;

          html += tr;
      })
    })

  } else {
    data.forEach(item => {
      let columnGroupOrTeacher = '';

      if (type === 'group') {
        columnGroupOrTeacher = item.teacher__fio;
      } else {
        columnGroupOrTeacher = item.group__name;
      }

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