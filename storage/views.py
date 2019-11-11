from django.shortcuts import render
from django.core.paginator import Paginator
from word_parse.parse import get_id_list_from_text
from django.http.response import HttpResponse
from .models import Vacancy
from django.template.loader import get_template


def vacancies(request):
    if request.method == 'POST':
        text = request.POST['text']

        id_vacancies = get_id_list_from_text(text)
        vacancy_list = Vacancy.objects.filter(id__in=id_vacancies).values('name', 'short_description', 'company',
                                                                          'salary_from', 'salary_to')
        print(vacancy_list)
        return render(request, 'vacancies.html', {'vacancy_list': vacancy_list})
    return render(request, 'home.html')
