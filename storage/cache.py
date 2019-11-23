import redis
from storage.core import get_id_dict_from_key_words
from word_parse.parse import lemmatization
from aggregator.settings import RESPONSE_CACHE_REDIS_HOST, RESPONSE_CACHE_REDIS_PORT, \
    WORD_CACHE_REDIS_HOST, WORD_CACHE_REDIS_PORT, QUERY_TEXT_CACHE_REDIS_HOST, QUERY_TEXT_CACHE_REDIS_PORT
from aggregator.celery import app


def get_response_from_cache(text):
    r = redis.Redis(host=RESPONSE_CACHE_REDIS_HOST, port=RESPONSE_CACHE_REDIS_PORT)
    key_words = lemmatization(text)
    processed_key_words = sorted(list(map(str.lower, key_words)))
    answer = r.zrange(str(processed_key_words), 0, -1)

    if answer:
        incr_query_text_to_cache.delay(text)
        incr_words_to_cache.delay(processed_key_words)
        return list(answer)
    else:

        answer = get_id_dict_from_key_words(key_words)
        incr_words_to_cache.delay(key_words)
        if answer:
            incr_query_text_to_cache.delay(text)
            r.zadd(str(processed_key_words), answer)

    return list(answer)


@app.task
def incr_words_to_cache(words):
    r = redis.Redis(host=WORD_CACHE_REDIS_HOST, port=WORD_CACHE_REDIS_PORT)
    for word in words:
        if r.exists(word):
            r.incr(word)
        else:
            r.set(word, 1)


@app.task
def incr_query_text_to_cache(query):
    r = redis.Redis(host=QUERY_TEXT_CACHE_REDIS_HOST, port=QUERY_TEXT_CACHE_REDIS_PORT)
    if r.exists(query):
        r.incr(query)
    else:
        r.set(query, 1)


def get_possible_query_list(cur_query):
    r = redis.Redis(host=QUERY_TEXT_CACHE_REDIS_HOST, port=QUERY_TEXT_CACHE_REDIS_PORT)
    possible_query_list = r.keys(cur_query + '*')
    possible_query_list.sort(key=lambda query: r.get(query))
    return [query.decode("utf-8") for query in possible_query_list]
