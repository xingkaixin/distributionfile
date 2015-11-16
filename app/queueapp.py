# -*- coding: utf-8 -*-


import redis
import json


class DogQueue(object):

    def __init__(self):

        self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=3)
        self.r.ping()

    def add(self, filepath):
        rs = self.r.exists(filepath)
        if rs:
            return True
        return self.r.set(filepath, '0')

    def getAll(self):
        return self.r.keys('*')

    def doing(self, filepath):
        return self.r.set(filepath, '0')

    def done(self, filepath):
        return self.r.expire(filepath, 0)

    def isConsuming(self, filepath):
        rs = self.r.get(filepath)
        if rs is None:
            return True
        elif rs == '0':
            return False
        else:
            return True
