# -*- coding: utf-8 -*-

import sys
import os
from celery import Celery
from conf import load_config
from celery import platforms


reload(sys)
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))

celery = Celery('PinPin',)

conf = load_config()

from beatjob import CELERYBEAT_SCHEDULE

celery.conf.update(
    BROKER_URL=conf.BROKER_URL,
    CELERY_RESULT_BACKEND=conf.CELERY_RESULT_BACKEND,
    CELERY_TASK_SERIALIZER=conf.CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=conf.CELERY_RESULT_SERIALIZER,
    CELERY_ACCEPT_CONTENT=conf.CELERY_ACCEPT_CONTENT,
    CELERY_TIMEZONE=conf.CELERY_TIMEZONE,
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE
)


platforms.C_FORCE_ROOT = True


import time
from core import logger
from fileroute import FileRoute
from queueapp import DogQueue


@celery.task(name="CheckFile")
def CheckFile(filepath, filesize=0):
    return _CheckFile(filepath, filesize)


def _CheckFile(filepath, filesize=0):
    logger.info('Checkfile........')
    from os.path import getsize

    newsize = getsize(filepath)
    logger.info('{filepath} size is {size}'.format(
        filepath=filepath, size=newsize))
    if newsize == filesize and newsize > 0:
        if newsize == 0:
            return False
        logger.info('Checkfile is Ok')
        f = FileRoute(filepath)
        try:
            logger.info('Check is is watchfile?')
            dest_path, filename = f.routeInfo()
            logger.info('{filepath} is our file'.format(filepath=filepath))
            q = DogQueue()
            q.add(filepath)
            logger.info('{filepath} add into Dogqueue'.format(
                filepath=filepath))
            return True
        except TypeError:
            logger.info('{filepath} is not our file'.format(filepath=filepath))
            return False
        except:
            logger.exception('_CheckFile')
            return False
        # UploadFile.apply_async(args=[filepath])
    logger.info('Checkfile is not Ok,pending {pendingtime} seconds'.format(
        pendingtime=conf.PENDING_TIME))
    time.sleep(conf.PENDING_TIME)
    return _CheckFile(filepath, newsize)


@celery.task(name="UploadFile")
def UploadFile(filepath):
    import shutil

    q = DogQueue()
    q.doing(filepath)
    f = FileRoute(filepath)
    try:
        logger.info('Send file to route')

        dest_path, filename = f.routeInfo()
        logger.info('Copy file {filepath} Begin'.format(filepath=filepath))
        shutil.copyfile(filepath, os.path.join(dest_path, filename))
        q.done(filepath)
    except TypeError:
        logger.info('{filepath} is not our file'.format(filepath=filepath))
        return False
    except:
        logger.exception('UploadFile')
        return False
    else:
        logger.info('Copy file {filepath} Success'.format(filepath=filepath))
        return True


@celery.task(name="DogQueueConsumer")
def DogQueueConsumer():

    logger.info('DogQueue consumer begin')
    q = DogQueue()
    try:
        rs = q.getAll()
        for r in rs:
            if not q.isConsuming(r):
                UploadFile.apply_async(args=[r])
                logger.info('DogQueue consuming {filepath}'.format(filepath=r))
    except:
        logger.exception('DogQueueConsumer')
    else:
        logger.info('DogQueue consumer end')
