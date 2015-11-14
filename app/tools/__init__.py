# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

flist = ['Nike_123', 'RPT_A_Nike_23123', 'RPT_A_23123','RPT_A_23123_ab','RPT_A','销售日报']

date = 'RPT_A_'

pattern = re.compile(r'^'+date+'[\_]?'+r'[A-Za-z0-9]*'+r'$')
for x in flist:
    match = pattern.search(x)
    if match:
        print x
