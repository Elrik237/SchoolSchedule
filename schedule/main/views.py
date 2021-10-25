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
        select_value = int(request.GET.get('selectValue'))
        select_date = request.GET.getlist('selectDate[]')

        date_from = datetime.datetime.strptime(select_date[0], '%Y-%m-%d')

        if len(select_date) == 1:
            schedule_list = Schedule.objects.filter(
                group = select_value,
                day = date_from
                ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('time')

        elif len(select_date) == 2:
            schedule_list = Schedule.objects.filter(
                group = select_value,
                day__range = select_date
                ).values('day', 'time', 'discipline', 'teacher', 'teacher__fio', 'group', 'group__name', 'place').order_by('day', 'time')

        data = json.dumps(list(schedule_list), default = customDateSerialize)

        return JsonResponse(data = data, safe=False)

