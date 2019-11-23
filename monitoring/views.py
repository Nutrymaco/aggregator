from django.shortcuts import render
from aggregator import settings
import redis


def cached_query(request):
    if request.method == 'GET':
        r = redis.Redis(host=settings.RESPONSE_CACHE_REDIS_HOST, port=settings.RESPONSE_CACHE_REDIS_PORT)
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
        r = redis.Redis(host=settings.INVERT_KEY_WORD_INDEX_REDIS_HOST, port=settings.INVERT_KEY_WORD_INDEX_REDIS_PORT)
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
        r = redis.Redis(host=settings.QUERY_TEXT_CACHE_REDIS_HOST, port=settings.QUERY_TEXT_CACHE_REDIS_PORT)
        redis_keys = r.keys('*')
        answer_dict = list()
        for key in redis_keys:
            answer_dict.append({
                'name': key.decode('utf-8'),
                'value': str(r.get(key))
            })
        return render(request, 'monitoring/list_keys.html', {'keys': answer_dict})