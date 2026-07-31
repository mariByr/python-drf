#цей файл це створення головного керівного обєкта селері -селері аpp
# os це модуль,бібліотека для взаємодії з операційною системою, а os.environ — його частина для роботи зі змінними середовища.
import os

from celery import Celery
from celery.schedules import crontab

# cтворення змінної середовища для налаштувань
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
#створення головного керівного обєкта селері -селері аpp
app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')#підключення до джанго і звідки бере налаштування

app.autodiscover_tasks() #шукає файли tasks.py у Django-застосунках
#періодичні задачі
app.conf.beat_schedule = {
    'send_spam_every_minutes':{

        'task': 'core.services.email_service.spam',
        'schedule': crontab()#для періодичності crontab guru
        # 'args': (),якщо функція яка тут виконується приймає арпгументи записуємо в аргс
    }
}