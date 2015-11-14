# -*- coding: utf-8 -*-


# from celery import Celery
# from .conf import load_config


# celery = Celery('PinPin',)

# conf = load_config()


# celery.conf.update(
#     BROKER_URL=conf.BROKER_URL,
#     CELERY_RESULT_BACKEND=conf.CELERY_RESULT_BACKEND,
#     CELERY_TASK_SERIALIZER=conf.CELERY_TASK_SERIALIZER,
#     CELERY_RESULT_SERIALIZER=conf.CELERY_RESULT_SERIALIZER,
#     CELERY_ACCEPT_CONTENT=conf.CELERY_ACCEPT_CONTENT,
#     CELERY_TIMEZONE=conf.CELERY_TIMEZONE
# )

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from conf import load_config

conf = load_config()

logger = logging.getLogger('distributionfile')
logger.setLevel(logging.DEBUG)


formatter = Formatter('%(asctime)s %(levelname)s: %(message)s ')

file_handler = RotatingFileHandler(conf.LOGFILE, maxBytes=10 * 1024 * 1024,
                                   backupCount=10)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
