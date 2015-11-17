# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from module import Base
from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
)


class FileRouteModule(Base):

    __tablename__ = 'app_file_route'

    id = Column(Integer, primary_key=True)
    src_path = Column(String(100))
    src_name = Column(String(100))
    src_extension = Column(String(50))
    retry_times = Column(Integer)
    retry_interval = Column(Integer)
    create_dt = Column(DateTime)
    update_dt = Column(DateTime)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    tar_path = Column(String(100))
    tar_name = Column(String(100))
    transtype = Column(String(100))
    ftpname = Column(String(100))

    def __repr__(self):
        return 'FileRouteModule {file_path}/{file_name}.{file_ext}'.format(file_path=self.src_path, file_name=self.src_name, file_ext=self.src_extension)
