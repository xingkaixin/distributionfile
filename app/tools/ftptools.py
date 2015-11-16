# -*- coding: utf-8 -*-


from abc import ABCMeta
import paramiko


class StandardFTPFactory(object):

    @staticmethod
    def get_factory(factory):
        if factory == 'FTP':
            return FTPFactory()
        elif factory == 'SFTP':
            return SFTPFactory()
        raise TypeError('Unknown Factory')


class FTPFactory(object):

    def get_client(self):
        return FTPClient()


class SFTPFactory(object):

    def get_client(self):
        return SFTPClient()


class BaseClient(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass


class SFTPClient(BaseClient):

    _t = None
    _sftp = None

    def __init__(self, host, username, password=None, key=None):
        if password and key:
            raise TypeError('either password or key')
        elif password is None and key is None:
            raise TypeError('either password or key')
        if key:
            raise SyntaxError('Not realized')
        self._t = paramiko.Transport((host, port))
        self._t.connect(username=username, password=password)
        self._sftp = paramiko.SFTPClient.from_transport(t)

    def put(self, local, remote):
        self._sftp.put(local, remote)

    def rename(self, old, new):
        self._sftp.rename(old, new)

    def close(self):
        self._t.close()
        self._t = None
        self._sftp = None


class FTPClient(BaseClient):
    pass
