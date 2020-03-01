from django.shortcuts import render
from aggregator import settings
import redis


def cached_query(request):
    if request.method == 'GET':
        r = redis.Redis(host=settings.REDIS_HOST, db=settings.RESPONSE_CACHE_REDIS_DB)
        redis_keys = r.keys('*')
        answer_dict = list()
        for key in redis_keys:
            answer_dict.append({
                'name': key.decode('utf-8'),
                'value': str(r.zrange(key, 0, -1))
            })
        return render(request, 'monitoring/list_keys.html', {'keys': answer_dict})


def key_words_invert_index(request):
    if request.method == 'GET':
        r = redis.Redis(host=settings.REDIS_HOST, db=settings.INVERT_KEY_WORD_INDEX_REDIS_DB)
        redis_keys = r.keys('*')
        answer_dict = list()
        for key in redis_keys:
            answer_dict.append({
                'name': key.decode('utf-8'),
                'value': r.smembers(key)
            })
        return render(request, 'monitoring/list_keys.html', {'keys': answer_dict})


def query_statistic(request):
    if request.method == 'GET':
        r = redis.Redis(db=settings.QUERY_TEXT_CACHE_REDIS_DB, host=settings.REDIS_HOST)
        redis_keys = r.keys('*')
        answer_dict = list()
        for key in redis_keys:
            answer_dict.append({
                'name': key.decode('utf-8'),
                'value': str(r.get(key))
            })
        return render(request, 'monitoring/list_keys.html', {'keys': answer_dict})