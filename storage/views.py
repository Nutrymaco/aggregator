from django.shortcuts import render
from django.core.paginator import Paginator
from storage.cache import get_response_from_cache, get_possible_query_list
from django.http.response import HttpResponse
from .models import Vacancy
from django.template.loader import get_template
import json


def vacancies(request):
    if request.method == 'POST':
        text = request.POST['text']

        id_vacancies = get_response_from_cache(text)
        vacancy_list = Vacancy.objects.filter(id__in=id_vacancies).values('name', 'short_description', 'company',
                                                                          'salary_from', 'salary_to')

        return render(request, 'vacancies.html', {'vacancy_list': vacancy_list})
    return render(request, 'home.html')


# API
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
            return HttpResponse({'{"items":[], "text":""'})