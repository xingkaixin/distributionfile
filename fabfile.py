#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *

env.user = 'boe'
env.hosts = ['10.8.4.116']




def pack():
    local('cd bin && dos2unix *.sh')
    tar_files = ['*.py','requirements.txt']
    tar_files.append('app/*')
    tar_files.append('bin/*.sh')
    local('rm -f www.tar.gz')
    local('tar -czvf www.tar.gz --exclude=\'*.tar.gz\' --exclude=\'.DS_Store\' --exclude=\'._.DS_Store\' --exclude=\'*.pyc\' --exclude=\'*.db\' --exclude=\'README.MD\' --exclude=\'*.log\' --exclude=\'fabfile.py\' %s' %
          ' '.join(tar_files))


def deploy():
    tarfile = 'www.tar.gz'
    remote_tmp_tar = '~/tmp/%s' % tarfile
    run('rm -f %s' % remote_tmp_tar)
    put('www.tar.gz', remote_tmp_tar)
    remote_dist_dir = '~/app1/'
    run('tar -xzvf %s -C %s' % (remote_tmp_tar, remote_dist_dir))


def release():
    execute(pack)
    execute(deploy)
