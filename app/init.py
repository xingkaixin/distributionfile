# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from module import (
    Base,
    engine,
    DBSession
)
from module.fileroute import FileRouteModule


# def init_repo():
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)


def update_repo():
    Base.metadata.create_all(engine)


def init_repo_data():
    import arrow
    import uuid
    session = DBSession()
    for i in range(1, 10):
        f = FileRouteModule()
        f.id = int(i)
        f.src_path = '/Users/Kevin/workspace/distributionfile/data'
        f.src_name = i
        f.src_extension = 'txt'
        f.retry_times = 0
        f.retry_interval = 0
        f.create_dt = arrow.utcnow().to('local').naive
        f.update_dt = arrow.utcnow().to('local').naive
        f.valid_from = arrow.utcnow().to('local').naive
        f.valid_to = arrow.utcnow().to('local').replace(days=365).naive
        f.tar_path = 'tmp/'
        f.tar_name = '{file}_{YMD}'.format(file=i, YMD='{YMD}')
        f.transtype = 'SFTP'
        f.ftpname = '10.8.4.116'
        session.add(f)

    f = session.query(FileRouteModule).get(9)
    f.tar_name = '9_{YM}'

    session.commit()
    session.close()




# session = DBSession()

# f = session.query(FileRouteModule).get(8)
# # f.src_path = '/Users/Kevin/workspace/distributionfile/data/nike'
# # f.src_name = u'销售日报'
# # f.src_extension = 'xls'
# # f.tar_path = 'tmp/nike/'
# # f.tar_name = u'销售日报_{YMD}'

# # session.commit()

# print f.src_name

# session.close()

# from tools.ftptools import StandardFTPFactory

# host = '10.8.4.116'
# port = 22
# username = 'boe'
# password = 'boe1234'

# f = StandardFTPFactory.get_factory('SFTP')
# c = f.get_client(host, port, username, password)


# local = 'init.py'

# remote = 'tmp/init_2011.py'

# temp = 'tmp/init_2011.py.transfering'


# c.put(local, temp)
# c.rename(temp, remote)
# c.close()


# from tools.ftptools import FTPInfo

# f = FTPInfo().get_info('10.8.4.116')
# print f
