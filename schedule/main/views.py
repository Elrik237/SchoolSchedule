from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, View

import pandas as pd

from django.contrib.staticfiles import finders

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = {'test': 'test'}
        return context

class SearchSchedule(View):
    def get(self, request):
        select_value = int(request.GET.get('selectValue'))
        select_date = request.GET.getlist('selectDate[]')


        data1 = [
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Иванов И.И.', 'place': 'Каб. 11'},
        ] 

        data2 = [
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Петров П.П.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Петров П.П.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Петров П.П.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Петров П.П.', 'place': 'Каб. 11'},
            {'time': '08:00 - 08:40', 'discipline': 'Родной язык', 'name': 'Петров П.П.', 'place': 'Каб. 11'},
        ]

        data = None

        if select_value == 1:
            data = data1
        elif select_value == 2:
            data = data2



        return JsonResponse(data = data, safe=False)

