from django.shortcuts import render
from django.core.paginator import Paginator
from storage.cache import get_response_from_cache, get_possible_query_list
from django.http.response import HttpResponse
from .models import Vacancy
from django.template.loader import get_template
import json


def vacancies(request):
    if request.method == 'GET':
        text = request.POST['text']

        id_vacancies = get_response_from_cache(text)
        vacancy_list = Vacancy.objects
            .filter(id__in=id_vacancies)
            .values('name', 'short_description', 'company', 'salary_from', 'salary_to', 'url')

        return render(request, 'vacancies.html', {'vacancy_list': vacancy_list})
    return render(request, 'index.html')


# API
# TODO - refactor with djangorestframework
def possible_query_list(request):
    if request.method == 'GET':
        try:
            cur_text = request.GET['text']
            query_list = get_possible_query_list(cur_text)
            answer = dict()
            answer['items'] = query_list
            answer['text'] = cur_text
            return HttpResponse(json.dumps(answer))
        except:
            return HttpResponse('{"items":[], "text":""')


def api_vacanices(request):
    if request.method == 'GET':
        text = request.POST['text']
        id_vacancies = get_response_from_cache(text)
        if not id_vacancies:
            return HttpResponse('{"items":[]}')
        vacancy_list = Vacancy.objects.filter(id__in=id_vacancies).values('name', 'short_description', 'company',
                                                                          'salary_from', 'salary_to', 'url')
        vacancy_dict = dict()
        vacancy_dict['items'] = list()
        if vacancy_list:
            for vacancy in vacancy_list:
                vacancy_dict['items'].append({
                    'name': vacancy.name,
                    'short_description': vacancy.short_description,
                    'company': vacancy.company,
                    'salary_from': vacancy.salary_from,
                    'salary_to': vacancy.salary_to,
                    'utl': vacancy.url
                })
            return HttpResponse(json.dumps(vacancy_dict))
        else:
            return HttpResponse('{"items":[]}')