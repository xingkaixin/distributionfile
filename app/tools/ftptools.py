# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from abc import ABCMeta
import paramiko
import os
import ConfigParser
import time


class FTPInfo(object):

    def __init__(self):
        basedir = os.path.dirname(os.path.dirname(
            os.path.abspath(os.path.dirname(__file__))))
        self.ftpconfig = os.path.join(basedir, 'ftp.conf')
        self.cf = ConfigParser.ConfigParser()

    def get_info(self, ftpname):
        with open(self.ftpconfig, 'r') as cfgfile:
            self.cf.readfp(cfgfile)
            selection = ftpname
            try:
                items = self.cf.options(selection)
            except ConfigParser.NoSectionError:
                items = None

            if items:

                rs = {}
                for item in items:
                    rs[item] = self.cf.get(selection, item)

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
        '''上传文件
        '''

        # 上传路径按"/"进行拆分
        remote_folders = remote.split('/')
        # 获得上传路径层级
        sub_folders_num = len(remote_folders)

        # 初始化层级数量为1，即为1时不存在子目录
        current_sub_folder_num = 1
        # 初始化层级递进次数，为0时不存在子目录
        cd_num = 0

        # 创建子目录
        for f in remote_folders:
            if current_sub_folder_num < sub_folders_num:
                try:
                    sftp.chdir(f)
                    cd_num += 1
                except IOError:
                    sftp.mkdir(f)
                    sftp.chdir(f)
                    cd_num += 1
                current_sub_folder_num += 1

        # 返回FTP登录目录
        if cd_num > 0:
            for i in range(cd_num):
                sftp.chdir('..')

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
