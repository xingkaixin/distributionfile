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
                                                          FileRouteModule.src_name == tempate_f).first()
                logger.debug(f)
                if f is None:
                    self.blocked = True
                    _f = session.query(FileRouteModule).filter(FileRouteModule.src_path == self._p,
                                                               FileRouteModule.src_name == '*', FileRouteModule.src_extension == self._ext).first()
                    if _f:
                        self.transtype = _f.transtype
                        self.ftpname = _f.ftpname
                        self.tar_path = _f.tar_path
                        self.tar_name = '{filenme}.{ext}'.format(
                            filename=self._f, ext=self._ext)
                        self.blocked = False
                elif f and f.src_extension.lower() != self._ext:
                    self.blocked = True
                else:
                    self.blocked = False

                    utcdt = arrow.utcnow().to('local')

                    # 目标目录生成
                    try:
                        tar_folder_dt_format_list = f.tar_folder_dt_format.split(
                            ',')
                        tar_folder_dt_format = tar_folder_dt_format_list[0]
                        tar_folder_dt_diff = int(tar_folder_dt_format_list[1])
                    except ValueError:
                        tar_folder_dt_diff = 0
                    except IndexError:
                        tar_folder_dt_diff = 0

                    if tar_folder_dt_format:
                        folder_timestamp = f.tar_path.format(DT=utcdt.replace(
                            days=tar_folder_dt_diff).format(tar_folder_dt_format))
                    else:
                        folder_timestamp = f.tar_path

                    self.tar_path = folder_timestamp

                    logger.debug(f.tar_name)
                    logger.debug(f.tar_dt_format)

                    # 目标文件名生成
                    try:
                        tar_dt_format_list = f.tar_dt_format.split(',')
                        tar_dt_format = tar_dt_format_list[0]
                        tar_dt_diff = int(tar_dt_format_list[1])
                    except ValueError:
                        tar_dt_diff = 0
                    except IndexError:
                        tar_dt_diff = 0
                    file_timestamp = f.tar_name.format(
                        DT=utcdt.replace(days=tar_dt_diff).format(tar_dt_format))
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
