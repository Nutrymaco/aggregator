from django.core.management.base import BaseCommand, CommandError
from aggregator import settings
import redis
from storage.models import Vacancy

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = redis.Redis(host=settings.INVERT_KEY_WORD_INDEX_REDIS_HOST, port=settings.INVERT_KEY_WORD_INDEX_REDIS_PORT)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=settings.WORD_CACHE_REDIS_HOST, port=settings.WORD_CACHE_REDIS_PORT)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=settings.RESPONSE_CACHE_REDIS_HOST, port=settings.RESPONSE_CACHE_REDIS_PORT)
        {r.delete(key) for key in r.keys('*')}
        r = redis.Redis(host=settings.QUERY_TEXT_CACHE_REDIS_HOST, port=settings.QUERY_TEXT_CACHE_REDIS_PORT)
        {r.delete(key) for key in r.keys('*')}
        Vacancy.objects.all().delete()


