from celery import Celery
from aggregator.celery_config import Config
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggregator.settings")
app = Celery()
app.config_from_object(Config)
