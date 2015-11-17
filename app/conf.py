# -*- coding: utf-8 -*-


import os


def load_config():
    mode = os.getenv('ENV', 'DEVELOPMENT')
    if mode == 'PRODUCTION':
        return Production
    elif mode == 'TEST':
        return Test
    else:
        return Development


class Config(object):
    DB_ENGINE = 'sqlite:///server.db'
    WATCH_PATH = '/Users/Kevin/workspace/distributionfile/data'
    PENDING_TIME = 2

    LOGFILE = 'log/sysout.log'

    # Celery
    BROKER_URL = 'redis://127.0.0.1:6379/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'


class Development(Config):
    pass


class Test(Config):
    DB_ENGINE = os.getenv('DWCONN')
    WATCH_PATH = '/home/boe/output'


class Production(Config):
    pass
