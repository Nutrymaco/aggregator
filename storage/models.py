from django.db import models


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    long_description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True, default='Worker')
    company = models.CharField(max_length=128, blank=True, null=True, default='Company')
    url = models.URLField(verbose_name='URL', default='https://hh.ru')
    salary_to = models.CharField(verbose_name='salary to', default='', max_length=10, null=True)
    salary_from = models.CharField(verbose_name='salary from', default='', max_length=10, null=True)

    class Meta:
        db_table = 'vacancy'

    def __str__(self):
        return self.name + ', ' + self.company