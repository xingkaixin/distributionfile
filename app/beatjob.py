from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {

    'DogQueueConsumer': {
        'task': 'DogQueueConsumer',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}
