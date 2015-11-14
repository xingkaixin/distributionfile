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


celery.conf.update(
    BROKER_URL=conf.BROKER_URL,
    CELERY_RESULT_BACKEND=conf.CELERY_RESULT_BACKEND,
    CELERY_TASK_SERIALIZER=conf.CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER=conf.CELERY_RESULT_SERIALIZER,
    CELERY_ACCEPT_CONTENT=conf.CELERY_ACCEPT_CONTENT,
    CELERY_TIMEZONE=conf.CELERY_TIMEZONE
)


platforms.C_FORCE_ROOT = True



import time
from core import logger

@celery.task(name="CheckFile")
def CheckFile(filepath, filesize=0):
    return _CheckFile(filepath, filesize)


def _CheckFile(filepath, filesize=0):
    logger.info('Checkfile........')
    from os.path import getsize
    newsize = getsize(filepath)
    logger.info('{filepath} size is {size}'.format(
        filepath=filepath, size=newsize))
    if newsize == filesize:
        if newsize == 0:
            return False
        logger.info('Checkfile is Ok')
        UploadFile.apply_async(args=[filepath])
        return True
    logger.info('Checkfile is not Ok,pending {pendingtime} seconds'.format(pendingtime=conf.PENDING_TIME))
    time.sleep(conf.PENDING_TIME)
    return _CheckFile(filepath, newsize)


@celery.task(name="UploadFile")
def UploadFile(filepath):
    import shutil
    from fileroute import FileRoute
    f = FileRoute(filepath)
    try:
        logger.info('Send file to route')
        dest_path, filename = f.routeInfo()
        logger.info('Copy file {filepath} Begin'.format(filepath=filepath))
        shutil.copyfile(filepath, os.path.join(dest_path, filename))
    except TypeError:
        logger.info('{filepath} isnot our file'.format(filepath=filepath))
        return False
    except:
        logger.exception('UploadFile')
        return False
    else:
        logger.info('Copy file {filepath} Success'.format(filepath=filepath))
        return True
