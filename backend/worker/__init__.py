# worker/__init__.py
import os
from dotenv import load_dotenv
from celery import Celery

# .env dosyasını yükle
load_dotenv()

# Celery uygulamasını tanımla
celery_app = Celery(
    'email_tasks',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
    include=['backend.worker.tasks']
)

# Timezone ayarı (Türkiye için)
celery_app.conf.timezone = 'Europe/Istanbul'