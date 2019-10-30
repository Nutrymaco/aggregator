from django.shortcuts import render
from word_parse.parse import get_id_list_from_text
from django.http.response import HttpResponse
# Create your views here.


def get_vacancies(request):
    if request.method == 'GET':
        return HttpResponse(get_id_list_from_text(request.GET['text']))