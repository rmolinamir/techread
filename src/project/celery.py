import os

from celery import Celery
from django.conf import settings

# TODO: Change this in production.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.project.settings.local")

app = Celery("techread")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
