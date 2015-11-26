# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from module.fileroute import FileRouteModule
from module import DBSession
import arrow
from core import logger
from tools.retools import getKeyName
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class FileRoute(object):

    blocked = False
    _filepath = None
    _p = None
    _f = None
    _ext = None

    transtype = None
    ftpname = None
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

        tempate_f = getKeyName(self._f)

        if tempate_f:
            try:
                f = session.query(FileRouteModule).filter(FileRouteModule.src_path == self._p,
                                                          FileRouteModule.src_name == tempate_f, FileRouteModule.src_extension == self._ext).first()
                logger.debug(f)
                if f is None:
                    self.blocked = True
                else:
                    self.blocked = False
                    self.tar_path = f.tar_path
                    utcdt = arrow.utcnow().to('local')
                    file_timestamp = f.tar_name.format(DT=utcdt.format(
                        f.tar_dt_format))
                    try:
                        file_timestamp = file_timestamp.decode('gbk')
                    except UnicodeDecodeError:
                        file_timestamp = unicode(file_timestamp).decode('gbk')
                    logger.debug(file_timestamp)
                    self.tar_name = '{filename}.{ext}'.format(
                        filename=file_timestamp, ext=f.src_extension)
                    self.transtype = f.transtype
                    self.ftpname = f.ftpname
            except:
                session.close()
                raise
            else:
                session.close()
        else:
            self.blocked = True
            logger.debug(
                'thi file name [{filename}] can re'.format(filename=self._f))

    def routeInfo(self):
        self._blocked()
        if self.blocked:
            return None
        logger.debug('Tar Path:{path},Tar File:{file}'.format(
            file=self.tar_name, path=self.tar_path))
        return self.transtype, self.ftpname, self.tar_path, self.tar_name
