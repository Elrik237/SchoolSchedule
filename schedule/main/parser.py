
import pandas as pd
from .models import Schedule, Teachers, Groups

class Parser():
    def __init__(self):
        self.parser_day()
        self.parser_quarter()       
        

    def parser_day(self):
        db_schedule = Schedule()
        db_teacher = Teachers ()
        db_group = Groups()


        schedule = pd.read_excel("D:\\Projects\\i_am\\table\\Raspisanie_klassy_ChETVERG_07_10.xlsx", 
                header=2, index_col=None, na_values=["NA"], na_filter = False)

        line_count = schedule.shape[0]

        groups  = schedule.columns.values.tolist()
        group_list = []

        for group in groups:
            if group != 'Время' and group != '№' and len(group) <= 3:
                group_list.append(group)

        column = 4

        
        for group in group_list:

            db_group.name = group

            db_group.save()

            print(f"Класс: {group}")
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
                        db_teacher.fio = {lesson[2]}

                        db_teacher.save()

                        db_schedule.day = "07.10.2021"
                        db_schedule.time = {lesson[0]}
                        db_schedule.discipline = {lesson[1]}
                        db_schedule.teacher = {lesson[2]}
                        db_schedule.group = group
                        db_schedule.place = {lesson[5]}
                        
                        db_schedule.save()

                        # print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                        #         f"Преподаватель: {lesson[2]}, Аудитория: {lesson[5]}")

                        count += 1
                        line += 2
                    elif len(lesson) == 10:
                        print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, " 
                                f"Аудитория: {lesson[7]} {lesson[3]} {lesson[9]}")
                        count += 1
                        line += 2
                    else:
                        if lesson[5]:
                            print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, " 
                                f"Аудитория: {lesson[9]} {lesson[3]} {lesson[11]} "
                                f"Предмет: {lesson[5]}, Преподаватель: {lesson[6]}, " 
                                f"Аудитория: {lesson[13]}")
                        else:
                            print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, " 
                                f"Аудитория: {lesson[9]} {lesson[3]} {lesson[11]} ")
                        count += 1
                        line += 2


            
            if  f"Unnamed: {column+3}" in schedule.columns and f"Unnamed: {column+5}" in schedule.columns:
                column += 6
            elif f"Unnamed: {column+3}" in schedule.columns:
                column += 4
            else:
                column += 2
        
        

    def parser_quarter(self):

        schedule = pd.read_excel("D:\\Projects\\i_am\\table\\Raspisanie_vse_klassy_1_chetvert.xlsx", 
                header = None, index_col=0, na_values=["NA"], na_filter = False)


        group_list = []

        for group in schedule.index.tolist():
            if type(group) == str and group != '№' and group != 'Расписание классов' and group != '':
                group_list.append(group)


        list_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье', ]
        

        width_colums = {}
        new_list_day_to_group = {}
        
        column_count = schedule.columns[-1]

        # первый столбец на день  
        for g in group_list:
            x = schedule[g:].head(3).values.tolist()
            column_start = 2
            width_colum = {}
            new_list_day =[]
            for i in x[2]:
                if i == "":
                    column_start +=1
                elif i in list_day:
                    width_colum[i] = [column_start,] 
                    width_colums[g] = width_colum
                    new_list_day.append(i)
                    column_start +=1

            new_list_day_to_group[g] = new_list_day # учебные дни для конкретной группы


        # последний столбец на день   
        for g in group_list:
            new_width_colums = width_colums
            count_day = 0
            for d in new_list_day_to_group[g]:
                try:
                    count_day +=1
                    next_day = new_list_day_to_group[g][count_day] # следующий день
                    first_column_next_day = new_width_colums[g][next_day][0] # первый столбец следующего дня у конкретного класса 
                    width_colums[g][d].append(first_column_next_day-1) # к индексу первого столбеца за конкретный день у конкретного класса 
                                                                    # добавляем  индекс последний
                except: 
                    pass


        count_group = 0

        for g in group_list:
            print(g)
            count_group +=1
            step = []
            y = width_colums[g]
            try:
                if g == group_list[-1]:
                    step = [g, None]
                else:
                    step = [g, group_list[count_group]]

                for d in new_list_day_to_group[g]:
                    print(d)
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
                                    place = full_lesson_info[index+1]
                                except:
                                    place = ""

                                if place == "":
                                    print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                    f"Преподаватель: {lesson[2]}, Аудитория: {place}")
                                else: 
                                    print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                    f"Преподаватель: {lesson[2]}, Аудитория: {place[2]}")
                                index += 1
                                count += 1
                                
                            elif len(lesson) == 5:
                                try:
                                    place = full_lesson_info[index+1]
                                except:
                                    place = ""
                                if place == "":
                                    print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                    f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place}")
                                else: 
                                    print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                    f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place[2]} "
                                                    f"{lesson[3]} {place[4]}")
                                index += 1
                                count += 1
                            else:
                                try:
                                    place = full_lesson_info[index+1]
                                except:
                                    place = ""

                                if lesson[5] != "":
                                    if place == "":
                                        print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                        f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place} "
                                                        f"Предмет: {lesson[5]}, " 
                                                        f"Преподаватель: {lesson[6]}, Аудитория: {place}")
                                    else: 
                                        print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                        f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place[2]} "
                                                        f"{lesson[3]} {place[4]} Предмет: {lesson[5]}, " 
                                                        f"Преподаватель: {lesson[6]}, Аудитория: {place[6]}")

                                else:
                                    if place == "":
                                        print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                        f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place}")
                                    else: 
                                        print(f"Урок №{count}, Время урока: {lesson[0]}, Предмет: {lesson[1]}, " 
                                                        f"Преподаватель: {lesson[2]} {lesson[3]} {lesson[4]}, Аудитория: {place[2]} {lesson[3]} {place[4]}")
                        
                                index += 1
                                count += 1
                        else:
                            index += 1
            
            except:
                print("Трабл")
                break
            
            

