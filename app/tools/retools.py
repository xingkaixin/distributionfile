# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import re

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# flist = ['Nike_123', 'RPT_A_Nike_23123',
#          'RPT_A_23123', 'RPT_A_23123_ab', 'RPT_A', '销售日报']

# date = 'RPT_A_'

# pattern = re.compile(r'^' + date + '[\_]?' + r'[A-Za-z0-9]*' + r'$')
# for x in flist:
#     match = pattern.search(x)
#     if match:
#         print x
# pattern = re.compile(r'^' +r'.*'+ '[\_]?' + r'[A-Za-z0-9]*' + r'$')
# match = pattern.match('Nike_123')
# if match:
#     print match.group()


# pattern = re.compile(r'.*[\_]')

# match = pattern.match('1_20151111')

# if match:
#     print match.group()[0:-1]


def getKeyName(name):
    try:
        pattern = re.compile(r'.*[\_]')
        match = pattern.match(name)
        if match:
            return match.group()[0:-1]
        return None
    except Exception as e:
        print e
        return None
