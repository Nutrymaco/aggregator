from django.core.management.base import BaseCommand, CommandError
from storage.cache import get_response_from_cache
from django.core.management.commands import runserver
from storage.models import Vacancy
from storage.tasks import write_to_cache
from word_parse.parse import delete_tags


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache_query_list = [
            'python junior',
            'js junior',
            'backend senior',
            'java разработчик',
            'стажировка python',
            'python backend junior',
            'javascript junior',
            'python django developer',
            'python',
            'js',
            'аналитик',
            'python intern',
            'python стажировка',
            'python flask',
            'pygam junior'
        ]
        '''
        for vacancy in Vacancy.objects.all():
            write_to_cache(delete_tags(vacancy.name) + " " + vacancy.long_description, vacancy.id)
            print(f'{vacancy.name} cached')
        '''

        for query in cache_query_list:
            get_response_from_cache(query)

