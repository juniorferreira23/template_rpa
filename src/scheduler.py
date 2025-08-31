from celery.schedules import crontab

from src.core.celery_app import celery_app

TIMEZONE = 'America/Sao_Paulo'

celery_app.conf.beat_schedule = {
    'get-stock-price-every-minute': {
        'task': 'src.tasks.hello',
        'schedule': crontab(minute='*'),
        'args': ('test',),
    },
    'run-example-bot-every-min': {
        'task': 'src.tasks.run_bot_example',
        'schedule': crontab(minute='*'),
        'args': (True,),
    },
}

celery_app.conf.update(timezone=TIMEZONE)
