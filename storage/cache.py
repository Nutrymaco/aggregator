import redis
from storage.core import get_id_dict_from_key_words
from word_parse.parse import lemmatization
from aggregator.settings import RESPONSE_CACHE_REDIS_DB, WORD_CACHE_REDIS_DB, COUPLE_WORD_REDIS_DB,\
    INVERT_KEY_WORD_INDEX_REDIS_DB, WORD_CACHE_REDIS_DB, INVERT_KEY_WORD_INDEX_REDIS_DB, \
    INVERT_TEXT_INDEX_REDIS_DB, QUERY_TEXT_CACHE_REDIS_DB, SYNONYM_WORD_REDIS_DB, REDIS_HOST
from aggregator.celery import app


def get_response_from_cache(text):
    r = redis.Redis(db=RESPONSE_CACHE_REDIS_DB, host=REDIS_HOST)
    key_words = lemmatization(text)

    if len(key_words) == 1:
        return get_cache_texts_id_for_word(key_words[0])

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
    r = redis.Redis(db=WORD_CACHE_REDIS_DB, host=REDIS_HOST)
    for word in words:
        if r.exists(word):
            r.incr(word)
        else:
            r.set(word, 1)


@app.task
def incr_query_text_to_cache(query):
    r = redis.Redis(db=QUERY_TEXT_CACHE_REDIS_DB, host=REDIS_HOST)
    if r.exists(query):
        r.incr(query)
    else:
        r.set(query, 1)


def get_possible_query_list(cur_query):
    r = redis.Redis(db=QUERY_TEXT_CACHE_REDIS_DB, host=REDIS_HOST)
    possible_query_list = r.keys(cur_query + '*')
    possible_query_list.sort(key=lambda query: r.get(query))
    return [query.decode("utf-8") for query in possible_query_list]


def get_cache_texts_id_for_word(word):
    r = redis.Redis(db=INVERT_KEY_WORD_INDEX_REDIS_DB, host=REDIS_HOST)
    value = r.smembers(word)
    if value:
        return value
    else:
        most_close_word = find_word_without_error_or_none(word)
        if most_close_word:
            return r.smembers(most_close_word)
        else:
            return []


def find_word_without_error_or_none(word_with_error):
    r = redis.Redis(db=WORD_CACHE_REDIS_DB, host=REDIS_HOST)
    words = list(key.decode('utf-8') for key in r.keys('*'))
    more_closer_word = (None, 0)
    for i in range(len(word_with_error)):
        for word in words:
            print(word, word[:i] + word[i+1:])
            if word_with_error[:i] + word_with_error[i + 1:] == word[:i] + word[i+1:]:
                val = r.get(word).decode('utf-8')
                if int(val) >= more_closer_word[1]:
                    more_closer_word = (word, val)

    return more_closer_word[0]
