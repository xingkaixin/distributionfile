# -*- coding: utf-8 -*-

from conf import load_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(load_config().DB_ENGINE)

DBSession = sessionmaker(bind=engine)




def transactional(fn):


    def transact(self,*args):
        session = DBSession()
        try:
            fn(self,session,*args)
            session.commit()
        except:
            session.rollback()
            raise


    transact.__name__ = fn.__name__
    return transact
