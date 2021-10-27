from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.contrib.staticfiles import finders
from django.db.models import *

import pandas as pd
import json 
import datetime

from .models import Schedule, Teachers,Groups

from operator import itemgetter
from itertools import groupby


def customDateSerialize(o):
    if isinstance(o, datetime.date):
        return o.__str__()


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        teachers = Teachers.objects.all()
        groups = Groups.objects.all()

        context = {'teachers': teachers, 'groups':groups}

        return context

class SearchSchedule(View):
    def get(self, request):
        select_group = int(request.GET.get('selectGroup'))
        select_teacher = int(request.GET.get('selectTeacher'))
        select_date = request.GET.getlist('selectDate[]')

        type_schedule = request.GET.get('type')

        if not select_date:
            return JsonResponse(data=[], safe=False)

        date_from = datetime.datetime.strptime(select_date[0], '%Y-%m-%d')

        if type_schedule == 'group':
            if len(select_date) == 1:

                schedule_list = Schedule.objects.filter(
                    group = select_group,
                    day = date_from
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('time')

                schedule_list = self.group(schedule_list)

            elif len(select_date) == 2:

                schedule_list = Schedule.objects.filter(
                    group = select_group,
                    day__range = select_date
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('day', 'time')



                schedule_list = self.group(schedule_list)


        if type_schedule == 'teacher':
            if len(select_date) == 1:
                schedule_list = Schedule.objects.filter(
                    teacher = select_teacher,
                    day = date_from
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('time')

                schedule_list = self.group(schedule_list)

            elif len(select_date) == 2:
                schedule_list = Schedule.objects.filter(
                    teacher = select_teacher,
                    day__range = select_date
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('day', 'time')
                
                schedule_list = self.group(schedule_list)

        data = json.dumps(list(schedule_list), default = customDateSerialize)

        return JsonResponse(data = data, safe=False)


    def group(self, items):

        if len(items) == 0:
            return []

        grouped_for_day_data = []
        grouped_data = []

        prev_item, full_items = items[0], items[1:]

        subgroup = [prev_item]
        
        for item in full_items:
            if item['day'] != prev_item['day']:
                grouped_for_day_data.append(subgroup)
                subgroup = []
            subgroup.append(item)
            prev_item = item
        grouped_for_day_data.append(subgroup)

        for item in grouped_for_day_data:
            if len(item) == 1:
                grouped_data.append([item])
                continue

            grouped_data.append([list(v) for k,v in groupby(item, key=itemgetter('time'))])

        return grouped_data