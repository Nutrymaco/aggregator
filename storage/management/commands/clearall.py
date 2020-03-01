from django.core.management.base import BaseCommand, CommandError
from aggregator import settings
import redis
from storage.models import Vacancy
from aggregator.settings import INVERT_KEY_WORD_INDEX_REDIS_DB, WORD_CACHE_REDIS_DB, RESPONSE_CACHE_REDIS_DB, \
    QUERY_TEXT_CACHE_REDIS_DB, REDIS_HOST

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = redis.Redis(host=REDIS_HOST, port=INVERT_KEY_WORD_INDEX_REDIS_DB)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=REDIS_HOST, port=WORD_CACHE_REDIS_DB)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=REDIS_HOST, port=RESPONSE_CACHE_REDIS_DB)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=REDIS_HOST, port=QUERY_TEXT_CACHE_REDIS_DB)
        {r.delete(key) for key in r.keys('*')}
        Vacancy.objects.all().delete()


