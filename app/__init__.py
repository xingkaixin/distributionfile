# -*- coding: utf-8 -*-

import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyFileMonitor(FileSystemEventHandler):

    def on_created(self, event):
        super(MyFileMonitor, self).on_created(event)
        if not event.is_directory:
            logging.info("created name:[{filepath}]".format(
                filepath=event.src_path))

    def on_modified(self, event):
        super(MyFileMonitor, self).on_created(event)
        if not event.is_directory:
            logging.info("modified name:[{filepath}]".format(
                filepath=event.src_path))
            CheckFileisOK(event.src_path)


def createDogService():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'D:\work\workspace\distributionfile\data'
    logging.info('DogService Start...')
    event_handler = MyFileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info('DogService Stop...')
    observer.join()


def CheckFileisOK(filename):
    from os.path import getsize
    logging.debug('{filename} size is {size}'.format(filename=filename,size=getsize(filename)))
