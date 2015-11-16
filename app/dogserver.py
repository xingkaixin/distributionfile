# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
from conf import load_config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from worker import CheckFile
from core import logger
from queueapp import DogQueue


conf = load_config()


q = DogQueue()


class MyFileMonitor(FileSystemEventHandler):

    def on_created(self, event):
        super(MyFileMonitor, self).on_created(event)
        if not event.is_directory:
            logger.info("created name:[{filepath}]".format(
                filepath=event.src_path))
            q.add(event.src_path)
            # CheckFile.apply_async(args=[event.src_path])

    def on_modified(self, event):
        super(MyFileMonitor, self).on_modified(event)
        if not event.is_directory:
            logger.info("modified name:[{filepath}]".format(
                filepath=event.src_path))
            q.add(event.src_path)
            # CheckFile.apply_async(args=[event.src_path])

    def on_moved(self, event):
        super(MyFileMonitor, self).on_moved(event)
        if not event.is_directory:
            logger.info("moved name:[{filepath}] to name:[{newfilepath}] ".format(
                filepath=event.src_path, newfilepath=event.dest_path))
            q.add(event.dest_path)
            # CheckFile.apply_async(args=[event.dest_path])


def createDogService():

    path = conf.WATCH_PATH
    logger.info('DogService Start...')
    event_handler = MyFileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info('DogService Stop...')
    except:
        logger.exception('DogService')
        observer.stop()
    observer.join()


if __name__ == '__main__':
    createDogService()
