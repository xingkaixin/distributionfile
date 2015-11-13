# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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
        super(MyFileMonitor, self).on_modified(event)
        if not event.is_directory:
            logging.info("modified name:[{filepath}]".format(
                filepath=event.src_path))
            if CheckFileisOK(event.src_path):
                UploadFile(event.src_path)

    def on_moved(self, event):
        super(MyFileMonitor, self).on_moved(event)
        if not event.is_directory:
            logging.info("moved name:[{filepath}] to name:[{newfilepath}] ".format(
                filepath=event.src_path, newfilepath=event.dest_path))
            if CheckFileisOK(event.dest_path):
                UploadFile(event.dest_path)


def createDogService():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'D:\\work\\workspace\\distributionfile\\data'
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


def CheckFileisOK(filepath, filesize=0):
    from os.path import getsize
    newsize = getsize(filepath)
    logging.debug('{filepath} size is {size}'.format(
        filepath=filepath, size=newsize))
    if newsize == filesize:
        logging.debug('Checkfile is Ok')
        return True
    logging.debug('Checkfile is not Ok,pending 10 seconds')
    time.sleep(2)
    if CheckFileisOK(filepath, newsize):
        return True


def UploadFile(filepath):
    import shutil
    from os.path import basename
    logging.info('Copy file {filepath} Begin'.format(filepath=filepath))
    dest_path = 'D:\\work\\workspace\\distributionfile\\fakehub\\{filename}'
    filename = basename(filepath)
    shutil.copyfile(filepath, dest_path.format(filename=filename))
    logging.info('Copy file {filepath} Success'.format(filepath=filepath))
