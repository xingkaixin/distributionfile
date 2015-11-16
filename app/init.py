# -*- coding: utf-8 -*-


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
        f.tar_path = '/Users/Kevin/workspace/distributionfile/fakehub'
        f.tar_name = '{file}_{YMD}'.format(file=i, YMD='{YMD}')
        session.add(f)

    f = session.query(FileRouteModule).get(9)
    f.tar_name = '9_{YM}'

    session.commit()
    session.close()



