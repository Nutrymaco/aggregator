from datetime import datetime
from celery.schedules import crontab

date = datetime.now()
hour, minute = date.hour, date.minute

beat_schedule = {
    # run in 2 minutes after running
    'recovery cache': {
        'task': 'storage.tasks.recovery',
        'schedule': crontab(hour=hour, minute=minute+2)
    },
    'scrape-and-index-regular': {
        'task': 'storage.tasks.scrape_and_index',
        'schedule': crontab(hour='*/6')
    }
}