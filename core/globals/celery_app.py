from datetime import timedelta
from celery import Celery
from core.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery('globals',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['globals.tasks'])

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'clear-expired-sessions': {
        'task': 'globals.tasks.clear_expired_sessions',
        'schedule': timedelta(days=1).total_seconds() ,  # every 30 seconds
    },
}
