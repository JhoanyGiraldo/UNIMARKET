from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Nombre del settings de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("mysite")

# Carga configuración desde settings.py con prefijo CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscovery de tareas en apps registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
