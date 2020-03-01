from aggregator.celery import app
from .models import Vacancy
import pymorphy2
from word_parse.parse import delete_tags
import requests
from datetime import datetime
import redis
import json
from aggregator.settings import INVERT_KEY_WORD_INDEX_REDIS_DB, REDIS_HOST


@app.task
def write_to_cache(text, text_index):
    morph = pymorphy2.MorphAnalyzer()
    text = delete_tags(text)
    r = redis.Redis(db=INVERT_KEY_WORD_INDEX_REDIS_DB, host=REDIS_HOST)
    for word in text.split(' '):
        if not word.isdigit():
            result = morph.parse(word)[0]
            if any(word_type in result.tag for word_type in
                   ['PREP', 'INTJ', 'PRCL', 'PRED', 'CONJ']):
                continue
            normal_word = result.normal_form
            r.sadd(normal_word, text_index)




# TODO: corutine transaction to db


# TO-DO: set up settings.py for redis
# TO-DO: add indexes and transactions
# TO-DO: refactor write to bd (create)
@app.task
def hh_scrapper(base_url='https://api.hh.ru/vacancies', start_shift=24*3600, specialization_list=[1]):
    now_datetime = datetime.now()
    time = now_datetime.timestamp()
    date = now_datetime.strftime("%Y-%m-%dT%H:%M:%S").__str__()
    response = requests.get(base_url, params={'specialization': specialization_list, 'per_page': 100}).json()
    vacancy_count = response['found']
    actual_id_vacancies_list = []


    if vacancy_count <= 2000:
        vacancy_list = response['items']
        vacancy_pages = response['pages']
        for page in range(1, vacancy_pages):
            response = requests.get(
                base_url, params={'page': page, 'specialization': specialization_list, 'per_page': 100}).json()
            vacancy_list[-1:] = response
            for vac in response['items']:
                response = json.loads(requests.get(vac['url']).json())

                if not Vacancy.objects.filter(id=response['id']):
                    # TODO: refactor db

                    if not response['salary']:
                        salary_from = salary_to = ''
                    else:
                        salary_from = response['salary']['from']
                        salary_to = response['salary']['to']

                        if salary_to == 'null':
                            salary_to = ''
                        elif salary_from == 'null':
                            salary_from = ''

                    description = delete_tags(response['description'])
                    vacancy = Vacancy.objects.create(name=response['name'], company=response['employer']['name'],
                                                     long_description=description,
                                                     short_description=description[:64],
                                                     id=response['id'], url=response['alternate_url'],
                                                     salary_to=salary_to, salary_from=salary_from)
                    vacancy.save()

                    # adding to redis cache
                    text_index = vacancy.id
                    text = vacancy.long_description

                    write_to_cache.delay(vacancy.name + ' ' + text, text_index)
                    actual_id_vacancies_list.append(text_index)

    else:
        vacancy_list = []
        while vacancy_count > 0:
            while True:
                response = requests.get(
                    base_url, params=
                    {'specialization': specialization_list,
                     'per_page': 100,
                     'date_from': datetime.fromtimestamp(time - start_shift).strftime("%Y-%m-%dT%H:%M:%S"),
                     'date_to': date
                     }).json()
                if response['found'] > 2000:
                    start_shift -= 3600
                else:
                    break

            for page in range(response['pages']):
                response = requests.get(
                    base_url, params=
                    {'specialization': specialization_list,
                     'per_page': 100,
                     'page': page,
                     'date_from': datetime.fromtimestamp(time - start_shift).strftime("%Y-%m-%dT%H:%M:%S"),
                     'date_to': date
                     }).json()
                vacancy_list[-1:] = response['items']
                vacancy_count -= len(response['items'])

                # final point
                for vac in response['items']:
                    response = requests.get(vac['url']).json()

                    if not Vacancy.objects.filter(id=response['id']):

                        if not response['salary']:
                            salary_from = salary_to = ''
                        else:
                            salary_to = response['salary']['to']
                            salary_from = response['salary']['from']
                            if salary_to == 'null':
                                salary_to = ''
                            elif salary_from == 'null':
                                salary_from = ''

                        description = delete_tags(response['description'])
                        vacancy = Vacancy.objects.create(name=response['name'], company=response['employer']['name'],
                                                         long_description=description,
                                                         short_description=description[:64],
                                                         id=response['id'], url=response['alternate_url'],
                                                         salary_to=salary_to, salary_from=salary_from)
                        vacancy.save()

                        # adding to redis cache
                        text_index = vacancy.id
                        text = vacancy.long_description

                        write_to_cache.delay(vacancy.name + ' ' + text, text_index)
                        actual_id_vacancies_list.append(text_index)

            date = datetime.fromtimestamp(time - start_shift).strftime("%Y-%m-%dT%H:%M:%S")
            time -= start_shift
            start_shift = 24*3600

    all_id_list = Vacancy.objects.values_list('id')
    id_to_delete = [id_v for id_v in all_id_list if id_v not in actual_id_vacancies_list]
    delete_vacancies.delay(id_to_delete)


@app.task
def delete_vacancies(id_to_delete):
    r = redis.Redis(host='redis', port=6379)

    # (не)транзакционно удаляем из редиса
    keys = r.keys('word_*')  # возможно потом тут будет word_
    for key in keys:
        for id in id_to_delete:
            r.hdel(key, id)

    # подчищаем бд
    for vacancy_id in id_to_delete:
        Vacancy.objects.get(id=vacancy_id).delete()


@app.task
def scrape_and_index():
    hh_scrapper.delay()


@app.task
def test_ping():
    from .schedules import beat_schedule
    print(beat_schedule['scrape-and-index-regular-1']['schedule'])
