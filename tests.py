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
ids = [row['id'] for row in rows]

print('Hydrating %d info objects...' % len(ids))

info_objs = ObjectFactory.get_by_ids(dbman, 'information_object', ids)

print('Finished! Iterating over them...')

io_list = []

n = 0
for io in info_objs: 
    io_list.append(io)

    n += 1
    if n % 100 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
print('Finished!')