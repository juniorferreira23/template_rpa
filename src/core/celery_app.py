from celery import Celery

from src.core.env import env

celery_app = Celery(
    main='tasks',
    broker=f'amqp://{env.USER_RABBITMQ}:{env.PASSWORD_RABBITMQ}@rabbitmq:5672//',
    backend='db+sqlite:///celery.sqlite',
)

# Importa/descobre as tasks
celery_app.autodiscover_tasks(['src.tasks'])
