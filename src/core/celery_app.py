from celery import Celery

from src.core.settings import settings

celery_app = Celery(
    main='tasks',
    broker=f'amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@rabbitmq:5672//',
    backend=(
        f'db+postgresql://{settings.POSTGRES_USER}'
        f':{settings.POSTGRES_PASSWORD}'
        f'@127.0.0.1:5432/{settings.POSTGRES_DB}'
    ),
)

# Importa/descobre as tasks
celery_app.autodiscover_tasks(['src.tasks'])
