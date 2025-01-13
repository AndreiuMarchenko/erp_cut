from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpsys.settings')
app = Celery('erpsys', broker_connection_retry=False,
             broker_connection_retry_on_startup=True, namespace='CELERY')
app.config_from_object('django.conf:settings')
broker_connection_retry = False
app.autodiscover_tasks()
