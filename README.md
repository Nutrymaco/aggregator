# aggregator
Web-application to search it-vacancies

Используемы технологии:
  1) Бэкенд - Django.
  2) Кэширования - Redis.
  3) Асинхронные задачи - Celery. 
  4) Обработка текста производится путем разбиения на слова, отбросом не несущих смысла частей речи (предлогов, союзов и т. д.), а затем лемматизации - приведения их в начальную форму.

Текущая схема приложения выглядит вот так:

![schema](https://github.com/Nutrymaco/aggregator/blob/master/Screenshot3.png)

