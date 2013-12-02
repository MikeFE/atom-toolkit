#!/usr/bin/env python3
"""
Quick and dirty tests for AtoM Toolkit development
"""

import config
import sys
import db

from model.object import *
from model.information_object import *
from factory import *
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_

cfg = config.Config('./config.json')

dbman = db.DatabaseManager(cfg)

c = dbman.get_connection()

io = dbman.table('information_object')
ioi = dbman.table('information_object_i18n')

sql = select([io.c.id]).where(io.c.id != 1)

rows = c.execute(sql)

print('Hydrating info objs')

ids = []

n = 0
for row in rows:
    ids.append(row['id'])
    n += 1
    if n == 10:
        break

for io in ObjectFactory.get_by_ids(dbman, 'information_object', ids):
    print(str(io))

print('\nDone! Got %d objects' % n)