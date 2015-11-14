# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from module.fileroute import FileRouteModule
from module import DBSession
import arrow
from core import logger


class FileRoute(object):

    blocked = False
    _filepath = None
    _p = None
    _f = None
    _ext = None

    tar_path = None
    tar_name = None

    def __init__(self, filepath):
        self._filepath = filepath

    def _blocked(self):
        self._p, self._f = os.path.split(self._filepath)
        self._f, self._ext = os.path.splitext(self._f)
        self._ext = self._ext.lower().replace('.', '')

        session = DBSession()

        logger.debug('Path:{path} File:{file}.{ext}'.format(
            path=self._p, file=self._f, ext=self._ext))

        f = session.query(FileRouteModule).filter(FileRouteModule.src_path == self._p,
                                                  FileRouteModule.src_name == self._f, FileRouteModule.src_extension == self._ext).first()
        logger.debug(f)
        if f is None:
            self.blocked = True
        else:
            self.blocked = False
            self.tar_path = f.tar_path
            utcdt = arrow.utcnow().to('local')
            self.tar_name = f.tar_name.format(YMD=utcdt.format(
                'YYYYMMDD'), YM=utcdt.format('YYYYMM')) + '.' + self._ext

    def routeInfo(self):
        self._blocked()
        if self.blocked:
            return None
        logger.debug('Tar Path:{path},Tar File:{file}'.format(
            file=self.tar_name, path=self.tar_path))
        return self.tar_path, self.tar_name
