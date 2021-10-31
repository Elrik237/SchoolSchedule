import os

from django.conf import settings
from .models import Schedule, Teachers, GroupsSchool
import pandas as pd

from isoweek import Week



class Parser():

    def start(self, event):
        
        name = (event.src_path.split('\\'))[-1]
        
        print(name)

        try:
            if "на день" in name:
                date = (name[-15:-5]).split('.')
                db_date = f"{date[2]}-{date[1]}-{date[0]}"
                self.parser_day(name, db_date)
            elif "на неделю" in name:
                x = (name.split('№'))[1] 
                y = (x.split('.'))[0]
                z = y.split('_')
                year = int(z[1])
                week = int(z[0])
                self.parser_quarter(name, year, week) 
            else:
                print("Не подходящий фомат excel")
        except Exception as e:
            print(e)

    def parser_day(self, name, date):

        try:
            schedule = pd.read_excel(f"{settings.MEDIA_ROOT}\\{name}", 
                header=2, index_col=None, na_values=["NA"], na_filter = False)


            line_count = schedule.shape[0]
            
            groups  = schedule.columns.values.tolist()
            group_list = []

            for group in groups:
                if group != 'Время' and group != '№' and len(group) <= 3:
                    group_list.append(group)

            save_group = GroupsSchool.objects.get_or_create(name = group)
            column = 4

            if len(group_list) != 0:
                for group in group_list:
                    print(f"Парсинг рассписания: {group}")

                    save_group = GroupsSchool.objects.get_or_create(name = group)

                    count = 1
                    line = 1

                    while line <= line_count:
                        lesson_info = []
                        lesson_time = []
                        full_lesson_info = []

                        lesson_info = schedule.loc[[line-1, line], group: f"Unnamed: {column}"]
                        lesson_time = schedule.loc[[line-1, line] , "Время"]

                        new_lesson_time = lesson_time.to_frame()

                        full_lesson_info = (pd.concat([new_lesson_time, lesson_info],  axis=1)).values.tolist()
                        

                        lesson= full_lesson_info[0] + full_lesson_info[1]

                        if lesson[1] == "":
                            count += 1
                            line += 2
                            continue
                        else:
                            if len(lesson) == 6:
                            
                                if (lesson[2])[-1] == '1':
                                    save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                    save_lesson = Schedule(day = date, time = lesson[0], discipline = f"{lesson[2]} (группа 1)",
                                                        teacher  = save_teacher[0], group = save_group[0], place = lesson[5])

                                    save_lesson.save()
                                elif (lesson[2])[-1] == '2':
                                    save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                    save_lesson = Schedule(day = date, time = lesson[0], discipline = f"{lesson[2]} (группа 2)",
                                                        teacher  = save_teacher[0], group = save_group[0], place = lesson[5])

                                    save_lesson.save()
                                else:
                                    save_teacher = Teachers.objects.get_or_create(fio = lesson[2])
                                    save_lesson = Schedule(day = date, time = lesson[0], discipline = lesson[1],
                                                        teacher  = save_teacher[0], group = save_group[0], place = lesson[5])

                                    save_lesson.save()
                                
                                

                                count += 1
                                line += 2
                            elif len(lesson) == 10:                    
                                try:
                                    if (lesson[2])[-1] == '1':
                                        get_teacher_one = (lesson[2])[0:-2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                    elif (lesson[2])[-1] == '2':
                                        get_teacher_two = lesson[2][0:-2]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                    else:
                                        get_teacher_one = lesson[2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                    if (lesson[4])[-1] == '1':
                                        get_teacher_one = (lesson[4])[0:-2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                    elif (lesson[4])[-1] == '2':
                                        get_teacher_two = lesson[4][0:-2]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                    else:
                                        get_teacher_two = lesson[4]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)


                                    if (lesson[7])[-1] == '1':
                                        get_place_one = (lesson[7])[0:-2]
                                        place_one = get_place_one
                                    elif (lesson[7])[-1] == '2':
                                        get_place_two = lesson[7][0:-2]
                                        place_two = get_place_two
                                    else:
                                        get_place_one = lesson[7]
                                        place_one = get_place_one

                                    if (lesson[9])[-1] == '1':
                                        get_place_one = (lesson[9])[0:-2]
                                        place_one = get_place_one
                                    elif (lesson[9])[-1] == '2':
                                        get_place_two = lesson[9][0:-2]
                                        place_two = get_place_two
                                    else:
                                        get_place_two = lesson[9]
                                        place_two = get_place_two

                                    save_lesson_one = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                        teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                    save_lesson_one.save()

                                    if lesson[3] != "/":
                                        save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{(lesson[3])[1:]} (группа 2)",
                                                            teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                        save_lesson_two.save()
                                    else:
                                        save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                            teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                        save_lesson_two.save()
                                    

                                except:
                                    if (lesson[2])[-1] == '1':
                                        save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                        save_lesson = Schedule(day = date, time = lesson[0], discipline = f"{lesson[2]} (группа 1)",
                                                            teacher  = save_teacher[0], group = save_group[0], place = place_one)

                                        save_lesson.save()
                                    elif (lesson[2])[-1] == '2':
                                        save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                        save_lesson = Schedule(day = date, time = lesson[0], discipline = f"{lesson[2]} (группа 2)",
                                                            teacher  = save_teacher[0], group = save_group[0], place = place_one)

                                        save_lesson.save()
                                    else:
                                        save_teacher = Teachers.objects.get_or_create(fio = lesson[2])
                                        save_lesson = Schedule(day = date, time = lesson[0], discipline = lesson[1],
                                                            teacher  = save_teacher[0], group = save_group[0], place = lesson[7])

                                        save_lesson.save()


                                count += 1
                                line += 2
                            else:
                                try:
                                    if (lesson[2])[-1] == '1':
                                        get_teacher_one = (lesson[2])[0:-2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                    elif (lesson[2])[-1] == '2':
                                        get_teacher_two = lesson[2][0:-2]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                    elif (lesson[2])[-1] == '3':
                                        get_teacher_three = lesson[2][0:-2]
                                        save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                    else:
                                        get_teacher_one = lesson[2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                    if (lesson[4])[-1] == '1':
                                        get_teacher_one = (lesson[4])[0:-2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                    elif (lesson[4])[-1] == '2':
                                        get_teacher_two = lesson[4][0:-2]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                    elif (lesson[4])[-1] == '3':
                                        get_teacher_three = lesson[2][0:-2]
                                        save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                    else:
                                        get_teacher_two = lesson[4]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)

                                    if (lesson[6])[-1] == '1':
                                        get_teacher_one = (lesson[6])[0:-2]
                                        save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                    elif (lesson[6])[-1] == '2':
                                        get_teacher_two = lesson[6][0:-2]
                                        save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                    elif (lesson[6])[-1] == '3':
                                        get_teacher_three = lesson[2][0:-2]
                                        save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                    else:
                                        get_teacher_three = lesson[6]
                                        save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)


                                    if (lesson[9])[-1] == '1':
                                        get_place_one = (lesson[9])[0:-2]
                                        place_one = get_place_one
                                    elif (lesson[9])[-1] == '2':
                                        get_place_two = lesson[9][0:-2]
                                        place_two = get_place_two
                                    elif (lesson[9])[-1] == '3':
                                        get_place_three = lesson[9][0:-2]
                                        place_three = get_place_three
                                    else:
                                        get_place_one = lesson[9]
                                        place_one = get_place_one

                                    if (lesson[11])[-1] == '1':
                                        get_place_one = (lesson[11])[0:-2]
                                        place_one = get_place_one
                                    elif (lesson[11])[-1] == '2':
                                        get_place_two = lesson[11][0:-2]
                                        place_two = get_place_two
                                    elif (lesson[11])[-1] == '3':
                                        get_place_three = lesson[11][0:-2]
                                        place_three = get_place_three
                                    else:
                                        get_place_two = lesson[11]
                                        place_two = get_place_two

                                    if (lesson[13])[-1] == '1':
                                        get_place_one = (lesson[13])[0:-2]
                                        place_one = get_place_one
                                    elif (lesson[13])[-1] == '2':
                                        get_place_two = lesson[13][0:-2]
                                        place_two = get_place_two
                                    elif (lesson[13])[-1] == '3':
                                        get_place_three = lesson[13][0:-2]
                                        place_three = get_place_three
                                    else:
                                        get_place_three = lesson[13]
                                        place_three = get_place_three

                                    save_lesson_one = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                        teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                    save_lesson_one.save()

                                    
                                    save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                        teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                    save_lesson_two.save()


                                    if lesson[5]:
                                        if (lesson[5])[0] == "/":
                                            save_lesson_three = Schedule(day = date, time = lesson[0], discipline = f"{(lesson[5])[1:-1]} (группа 3)",
                                                                teacher  = save_teacher_three[0], group = save_group[0], place = place_three)

                                            save_lesson_three.save()
                                        else:
                                            save_lesson_three = Schedule(day = date, time = lesson[0], discipline = f"{lesson[5]} (группа 3)",
                                                                teacher  = save_teacher_three[0], group = save_group[0], place = place_three)

                                            save_lesson_three.save()

                                except:
                                    try:
                                        if (lesson[2])[-1] == '1':
                                            get_teacher_one = (lesson[2])[0:-2]
                                            save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                        elif (lesson[2])[-1] == '2':
                                            get_teacher_two = lesson[2][0:-2]
                                            save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                        else:
                                            get_teacher_one = lesson[2]
                                            save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                        if (lesson[4])[-1] == '1':
                                            get_teacher_one = (lesson[4])[0:-2]
                                            save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                        elif (lesson[4])[-1] == '2':
                                            get_teacher_two = lesson[4][0:-2]
                                            save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                        else:
                                            get_teacher_two = lesson[4]
                                            save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)


                                        if (lesson[9])[-1] == '1':
                                            get_place_one = (lesson[9])[0:-2]
                                            place_one = get_place_one
                                        elif (lesson[9])[-1] == '2':
                                            get_place_two = lesson[9][0:-2]
                                            place_two = get_place_two
                                        else:
                                            get_place_one = lesson[9]
                                            place_one = get_place_one

                                        if (lesson[11])[-1] == '1':
                                            get_place_one = (lesson[11])[0:-2]
                                            place_one = get_place_one
                                        elif (lesson[11])[-1] == '2':
                                            get_place_two = lesson[11][0:-2]
                                            place_two = get_place_two
                                        else:
                                            get_place_two = lesson[11]
                                            place_two = get_place_two

                                        save_lesson_one = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                            teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                        save_lesson_one.save()


                                        if lesson[5]:
                                            if (lesson[5])[0] == "/":
                                                save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{(lesson[5])[1:-1]} (группа 2)",
                                                                    teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                                save_lesson_two.save()
                                            else:
                                                save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{lesson[5]} (группа 2)",
                                                                    teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                                save_lesson_two.save()
                                        else:
                                            save_lesson_two = Schedule(day = date, time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                            save_lesson_two.save()
                                    

                                    except:
                                        save_teacher = Teachers.objects.get_or_create(fio = lesson[2])

                                        save_lesson = Schedule(day = date, time = lesson[0], discipline = lesson[1],
                                                                teacher  = save_teacher[0], group = save_group[0], place = lesson[9])

                                        save_lesson.save()


                                count += 1
                                line += 2
            
                    if  f"Unnamed: {column+3}" in schedule.columns and f"Unnamed: {column+5}" in schedule.columns:
                        column += 6
                    elif f"Unnamed: {column+3}" in schedule.columns:
                        column += 4
                    else:
                        column += 2
            else:
                print("Ошибка парсинга. Проверьте оформление\содержание документа или название файла")    
        except Exception as e:
            print(e)


    def parser_quarter(self, name, year, week):

        try:
            schedule = pd.read_excel(f"{settings.MEDIA_ROOT}\\{name}", 
                    header = None, index_col=0, na_values=["NA"], na_filter = False)


            group_list = []

            for group in schedule.index.tolist():
                if type(group) == str and group != '№' and group != 'Расписание классов' and group != '':
                    group_list.append(group)


            list_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', ]      

            width_colums = {}
            new_list_day_to_group = {}

            # первый столбец на день  
            for group in group_list:
                x = schedule[group:].head(3).values.tolist()
                column_start = 2
                width_colum = {}
                new_list_day =[]
                for i in x[2]:
                    if i == "":
                        column_start +=1
                    elif i in list_day:
                        width_colum[i] = [column_start,] 
                        width_colums[group] = width_colum
                        new_list_day.append(i)
                        column_start +=1

                new_list_day_to_group[group] = new_list_day # учебные дни для конкретной группы


            # последний столбец на день   
            for group in group_list:

                new_width_colums = width_colums
                count_day = 0
                for d in new_list_day_to_group[group]:
                    try:
                        count_day +=1
                        next_day = new_list_day_to_group[group][count_day] # следующий день
                        first_column_next_day = new_width_colums[group][next_day][0] # первый столбец следующего дня у конкретного класса 
                        width_colums[group][d].append(first_column_next_day-1) # к индексу первого столбеца за конкретный день у конкретного класса 
                                                                        # добавляем  индекс последний
                    except: 
                        pass


            count_group = 0
            
            if len(width_colums) != 0:
                for group in group_list:
                    print(f"Парсинг рассписания: {group}")

                    save_group = GroupsSchool.objects.get_or_create(name = group)

                    count_group +=1
                    step = []
                    y = width_colums[group]
                    try:
                        if group == group_list[-1]:
                            step = [group, None]
                        else:
                            step = [group, group_list[count_group]]

                        for d in new_list_day_to_group[group]:
                            count = 1
                            index = 0
                            if len(y[d]) == 2:
                                lesson_info = schedule.loc[step[0] : step[1], y[d][0] : y[d][1]]
                            else:
                                lesson_info = schedule.loc[step[0] : step[1], y[d][0] :]

                            lesson_time = schedule.loc[step[0] : step[1] , 1]

                            new_lesson_time = lesson_time.to_frame()

                            full_lesson_info = (pd.concat([new_lesson_time, lesson_info],  axis=1)).values.tolist()
                            
                            for lesson in full_lesson_info:
                                if lesson[0] != '' and lesson[0] != 'Время' and lesson[1] != '':
                                    if len(lesson) == 3:
                                        try:
                                            place = (full_lesson_info[index+1])[2]
                                        except:
                                            place = ""

                                        if (lesson[2])[-1] == '1':
                                            save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                            save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                                teacher  = save_teacher[0], group = save_group[0], place = place)
                                            save_lesson.save()
                                        elif (lesson[2])[-1] == '2':
                                            save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                            save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                teacher  = save_teacher[0], group = save_group[0], place = place)
                                            save_lesson.save()
                                        else:
                                            save_teacher = Teachers.objects.get_or_create(fio = lesson[2])
                                            save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = lesson[1],
                                                                teacher  = save_teacher[0], group = save_group[0], place = place)

                                            save_lesson.save()
                                        index += 1
                                        count += 1     
                                    elif len(lesson) == 5:
                                        try:
                                            place = full_lesson_info[index+1]

                                            if (place[2])[-1] == '1':
                                                get_place_one = (place[2])[0:-2]
                                                place_one = get_place_one
                                            elif (place[2])[-1] == '2':
                                                get_place_two = place[2][0:-2]
                                                place_two = get_place_two
                                            else:
                                                get_place_one = place[2]
                                                place_one = get_place_one

                                            if (place[4])[-1] == '1':
                                                get_place_one = (place[4])[0:-2]
                                                place_one = get_place_one
                                            elif (place[4])[-1] == '2':
                                                get_place_two = place[4][0:-2]
                                                place_two = get_place_two
                                            else:
                                                get_place_two = place[4]
                                                place_two = get_place_two
                                        except:
                                            try:
                                                place_one = (full_lesson_info[index+1])[2]
                                                place_two = ""
                                            except:
                                                place_one = ""
                                                place_two = ""
                                        
                                        
                                        try:
                                            if (lesson[2])[-1] == '1':
                                                get_teacher_one = (lesson[2])[0:-2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                            elif (lesson[2])[-1] == '2':
                                                get_teacher_two = lesson[2][0:-2]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                            else:
                                                get_teacher_one = lesson[2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                            if (lesson[4])[-1] == '1':
                                                get_teacher_one = (lesson[4])[0:-2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                            elif (lesson[4])[-1] == '2':
                                                get_teacher_two = lesson[4][0:-2]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                            else:
                                                get_teacher_two = lesson[4]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)


                                            

                                            save_lesson_one = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                                teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                            save_lesson_one.save()

                                            save_lesson_two = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                            save_lesson_two.save()
                                            
                                        except:
                                            if (lesson[2])[-1] == '1':
                                                save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                                save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[2]} (группа 1)",
                                                                    teacher  = save_teacher[0], group = save_group[0], place = place_one)

                                                save_lesson.save()
                                            elif (lesson[2])[-1] == '2':
                                                save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                                save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[2]} (группа 2)",
                                                                    teacher  = save_teacher[0], group = save_group[0], place = place_two)

                                                save_lesson.save()
                                            else:
                                                save_teacher = Teachers.objects.get_or_create(fio = lesson[2])
                                                save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = lesson[1],
                                                                    teacher  = save_teacher[0], group = save_group[0], place = place_one)

                                                save_lesson.save()

                                            
                                        index += 1
                                        count += 1
                                    else:
                                        try:
                                            place = full_lesson_info[index+1]
                                            if lesson[5] != "":
                                                if (place[2])[-1] == '1':
                                                    get_place_one = (place[2])[0:-2]
                                                    place_one = get_place_one
                                                elif (place[2])[-1] == '2':
                                                    get_place_two = place[2][0:-2]
                                                    place_two = get_place_two
                                                elif (place[2])[-1] == '3':
                                                    get_place_three = place[2][0:-2]
                                                    place_three = get_place_three
                                                else:
                                                    get_place_one = place[2]
                                                    place_one = get_place_one

                                                if (place[4])[-1] == '1':
                                                    get_place_one = (place[4])[0:-2]
                                                    place_one = get_place_one
                                                elif (place[4])[-1] == '2':
                                                    get_place_two = place[4][0:-2]
                                                    place_two = get_place_two
                                                elif (place[4])[-1] == '3':
                                                    get_place_three = place[4][0:-2]
                                                    place_three = get_place_three
                                                else:
                                                    get_place_two = place[4]
                                                    place_two = get_place_two

                                                if (place[6])[-1] == '1':
                                                    get_place_one = (place[6])[0:-2]
                                                    place_one = get_place_one
                                                elif (place[6])[-1] == '2':
                                                    get_place_two = place[6][0:-2]
                                                    place_two = get_place_two
                                                elif (place[6])[-1] == '3':
                                                    get_place_three = place[6][0:-2]
                                                    place_three = get_place_three
                                                else:
                                                    get_place_three = place[6]
                                                    place_three = get_place_three
                                            else:
                                                if (place[2])[-1] == '1':
                                                    get_place_one = (place[2])[0:-2]
                                                    place_one = get_place_one
                                                elif (place[2])[-1] == '2':
                                                    get_place_two = place[2][0:-2]
                                                    place_two = get_place_two
                                                else:
                                                    get_place_one = place[2]
                                                    place_one = get_place_one

                                                if (place[4])[-1] == '1':
                                                    get_place_one = (place[4])[0:-2]
                                                    place_one = get_place_one
                                                elif (place[4])[-1] == '2':
                                                    get_place_two = place[4][0:-2]
                                                    place_two = get_place_two
                                                else:
                                                    get_place_two = place[4]
                                                    place_two = get_place_two
                                        
                                        except:
                                            place_one = ""
                                            place_two= ""
                                            place_three = ""
                                            
                                        
                                        try:
                                            if (lesson[2])[-1] == '1':
                                                get_teacher_one = (lesson[2])[0:-2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                            elif (lesson[2])[-1] == '2':
                                                get_teacher_two = lesson[2][0:-2]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                            elif (lesson[2])[-1] == '3':
                                                get_teacher_three = lesson[2][0:-2]
                                                save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                            else:
                                                get_teacher_one = lesson[2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                            if (lesson[4])[-1] == '1':
                                                get_teacher_one = (lesson[4])[0:-2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                            elif (lesson[4])[-1] == '2':
                                                get_teacher_two = lesson[4][0:-2]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                            elif (lesson[4])[-1] == '3':
                                                get_teacher_three = lesson[2][0:-2]
                                                save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                            else:
                                                get_teacher_two = lesson[4]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)

                                            if (lesson[6])[-1] == '1':
                                                get_teacher_one = (lesson[6])[0:-2]
                                                save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                            elif (lesson[6])[-1] == '2':
                                                get_teacher_two = lesson[6][0:-2]
                                                save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                            elif (lesson[6])[-1] == '3':
                                                get_teacher_three = lesson[2][0:-2]
                                                save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)
                                            else:
                                                get_teacher_three = lesson[6]
                                                save_teacher_three = Teachers.objects.get_or_create(fio = get_teacher_three)


                                        

                                            save_lesson_one = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                                teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                            save_lesson_one.save()

                                            
                                            save_lesson_two = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                            save_lesson_two.save()


                                            if lesson[5]:
                                                if (lesson[5])[0] == "/":
                                                    save_lesson_three = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{(lesson[5])[1:-1]} (группа 3)",
                                                                        teacher  = save_teacher_three[0], group = save_group[0], place = place_three)

                                                    save_lesson_three.save()
                                                else:
                                                    save_lesson_three = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[5]} (группа 3)",
                                                                        teacher  = save_teacher_three[0], group = save_group[0], place = place_three)

                                                    save_lesson_three.save()

                                        except:
                                            try:
                                                try:
                                                    place = full_lesson_info[index+1]

                                                    if (place[2])[-1] == '1':
                                                        get_place_one = (place[2])[0:-2]
                                                        place_one = get_place_one
                                                    elif (place[2])[-1] == '2':
                                                        get_place_two = place[2][0:-2]
                                                        place_two = get_place_two
                                                    else:
                                                        get_place_one = place[2]
                                                        place_one = get_place_one

                                                    if (place[4])[-1] == '1':
                                                        get_place_one = (place[4])[0:-2]
                                                        place_one = get_place_one
                                                    elif (place[4])[-1] == '2':
                                                        get_place_two = place[4][0:-2]
                                                        place_two = get_place_two
                                                    else:
                                                        get_place_two = place[4]
                                                        place_two = get_place_two
                                                except:
                                                    place_one = ""
                                                    place_two= ""
                                            
                                                if (lesson[2])[-1] == '1':
                                                    get_teacher_one = (lesson[2])[0:-2]
                                                    save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                                elif (lesson[2])[-1] == '2':
                                                    get_teacher_two = lesson[2][0:-2]
                                                    save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                                else:
                                                    get_teacher_one = lesson[2]
                                                    save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)

                                                if (lesson[4])[-1] == '1':
                                                    get_teacher_one = (lesson[4])[0:-2]
                                                    save_teacher_one = Teachers.objects.get_or_create(fio = get_teacher_one)
                                                elif (lesson[4])[-1] == '2':
                                                    get_teacher_two = lesson[4][0:-2]
                                                    save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)
                                                else:
                                                    get_teacher_two = lesson[4]
                                                    save_teacher_two = Teachers.objects.get_or_create(fio = get_teacher_two)


                                                save_lesson_one = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                                    teacher  = save_teacher_one[0], group = save_group[0], place = place_one)

                                                save_lesson_one.save()


                                                if lesson[5]:
                                                    if (lesson[5])[0] == "/":
                                                        save_lesson_two = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{(lesson[5])[1:-1]} (группа 2)",
                                                                            teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                                        save_lesson_two.save()
                                                    else:
                                                        save_lesson_two = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[5]} (группа 2)",
                                                                            teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                                        save_lesson_two.save()
                                                else:
                                                    save_lesson_two = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                        teacher  = save_teacher_two[0], group = save_group[0], place = place_two)

                                                    save_lesson_two.save()
                                            
                                            except:
                                                try:
                                                    place = (full_lesson_info[index+1])[2]
                                                except:
                                                    place = ""

                                                if (lesson[2])[-1] == '1':
                                                    save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                                    save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 1)",
                                                                        teacher  = save_teacher[0], group = save_group[0], place = place)

                                                    save_lesson.save()
                                                elif (lesson[2])[-1] == '2':
                                                    save_teacher = Teachers.objects.get_or_create(fio = (lesson[2])[0:-2])
                                                    save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = f"{lesson[1]} (группа 2)",
                                                                        teacher  = save_teacher[0], group = save_group[0], place = place)

                                                    save_lesson.save()
                                                else:
                                                    save_teacher = Teachers.objects.get_or_create(fio = lesson[2])
                                                    save_lesson = Schedule(day = self.get_date(d, year, week), time = lesson[0], discipline = lesson[1],
                                                                        teacher  = save_teacher[0], group = save_group[0], place = place)

                                                
                                                index += 1
                                                count += 1
                                
                                else:
                                    index += 1
                    
                    except:
                        print("Ошибка парсинга. Проверьте оформление\содержание документа или название файла")
                        break
            else:
                print("Ошибка парсинга. Проверьте оформление\содержание документа или название файла")              
        except Exception as e:
            print(e)        
            
    def get_date(self, day, year, week):

        if day == "Понедельник":
            return Week(year, week).monday()
        elif day == "Вторник":
            return Week(year, week).tuesday()
        elif day == "Среда":
            return Week(year, week).wednesday()
        elif day == "Четверг":
            return Week(year, week).thursday()
        elif day == "Пятница":
            return Week(year, week).friday()
        elif day == "Суббота":
            return Week(year, week).saturday()
        elif day == "Воскресенье":
            return Week(year, week).sunday()
