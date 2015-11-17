# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from abc import ABCMeta
import paramiko
import os
import ConfigParser
import time


class FTPInfo(object):

    def __init__(self):
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        self.ftpconfig = os.path.join(basedir, 'ftp.conf')
        self.cf = ConfigParser.ConfigParser()

    def get_info(self,ftpname):
        with open(self.ftpconfig,'r') as cfgfile:
            self.cf.readfp(cfgfile)
            selection = ftpname
            try:
                items = self.cf.options(selection)
            except ConfigParser.NoSectionError:
                items = None

            if items:

                rs = {}
                for item in items:
                    rs[item] = self.cf.get(selection,item)

                return rs
            return None




class StandardFTPFactory(object):

    @staticmethod
    def get_factory(factory):
        if factory == 'FTP':
            return FTPFactory()
        elif factory == 'SFTP':
            return SFTPFactory()
        raise TypeError('Unknown Factory')


class FTPFactory(object):

    def get_client(self, host, port, username, password=None, key=None):
        return FTPClient(host, port, username, password, key)


class SFTPFactory(object):

    def get_client(self, host, port, username, password=None, key=None):
        return SFTPClient(host, port, username, password, key)


class BaseClient(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass


class SFTPClient(BaseClient):

    _t = None
    _sftp = None

    def __init__(self, host, port, username, password=None, key=None):
        if password and key:
            raise TypeError('either password or key')
        elif password is None and key is None:
            raise TypeError('either password or key')
        if key:
            raise SyntaxError('Not realized')
        self._t = paramiko.Transport((host, port))
        self._t.connect(username=username, password=password)
        self._sftp = paramiko.SFTPClient.from_transport(self._t)

    def put(self, local, remote):
        self._sftp.put(local, remote)

    def rename(self, old, new):
        try:
            self._sftp.remove(new)
        except IOError:
            self._sftp.rename(old, new)
        else:
            self._sftp.rename(old, new)

    def close(self):
        self._t.close()
        self._t = None
        self._sftp = None


class FTPClient(BaseClient):
    pass
