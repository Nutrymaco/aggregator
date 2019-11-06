from storage.schedules import beat_schedule as schedule


class Config:
    timezone = 'Europe/Moscow'
    broker_transport = "redis"
    broker_vhost = 0  # Maps to redis host.
    broker_port = 6379  # Maps to redis port.
    broker_host = "127.0.0.1"  # Maps to database number.
    celery_ignore_result = True
    enable_utc = True
    imports = ('storage.tasks',)
    beat_schedule = schedule
    django_settings_module = '/Users/smykovefim/MyProjects/Django/aggregator/aggregator/settings.py'


