from datetime import datetime
from celery.schedules import crontab

date = datetime.now()
hour, minute = date.hour, date.minute
hour = (hour + (minute + 3) // 60 + 3) % 24
beat_schedule = {
    'scrape-and-index-regular-1': {
        'task': 'storage.tasks.scrape_and_index',
        'schedule': crontab(hour=hour, minute=(minute+1) % 60)
    },
    'scrape-and-index-regular-2': {
        'task': 'storage.tasks.scrape_and_index',
        'schedule': crontab(hour=(hour + 6) % 24)
    },
    'scrape-and-index-regular-3': {
        'task': 'storage.tasks.scrape_and_index',
        'schedule': crontab(hour=(hour + 12) % 24)
    },
    'scrape-and-index-regular-4': {
        'task': 'storage.tasks.scrape_and_index',
        'schedule': crontab(hour=(hour + 18) % 24)
    },
    'ping':{
        'task': 'storage.tasks.test_ping',
        'schedule': crontab()

    }

}
