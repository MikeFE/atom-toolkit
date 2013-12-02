#!/usr/bin/env python3
"""
Quick and dirty tests for AtoM Toolkit development
"""

import config
import db

from model.object import *
from model.information_object import *
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_

cfg = config.Config('./config.json')

dbman = db.DatabaseManager(cfg)

c = dbman.get_connection()

io = dbman.table('information_object')
ioi = dbman.table('information_object_i18n')

sql = select([io.c.id]).where(io.c.id != 1)

rows = c.execute(sql)

n = 0
for row in rows:
    o = InformationObject(dbman)
    o.hydrate(id=row['id'])
    for c in o.has_cultures:
        print(repr(getattr(o, c).__dict__))
    n += 1
    if n == 1:
        break