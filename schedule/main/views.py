from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.contrib.staticfiles import finders

import pandas as pd
import json 
import datetime

from .models import Schedule, Teachers,Groups


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

            elif len(select_date) == 2:
                schedule_list = Schedule.objects.filter(
                    group = select_group,
                    day__range = select_date
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('day', 'time')

        if type_schedule == 'teacher':
            if len(select_date) == 1:
                schedule_list = Schedule.objects.filter(
                    teacher = select_teacher,
                    day = date_from
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('time')

            elif len(select_date) == 2:
                schedule_list = Schedule.objects.filter(
                    teacher = select_teacher,
                    day__range = select_date
                    ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('day', 'time')


        data = json.dumps(list(schedule_list), default = customDateSerialize)

        return JsonResponse(data = data, safe=False)

