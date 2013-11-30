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

sql = select([io, ioi], use_labels=True).where(
    and_(
        io.c.id == ioi.c.id,
        ioi.c.title != None
    )
)

rows = c.execute(sql)

n = 0
for row in rows:
    o = InformationObject(dbman)
    o.hydrate(row)
    print(o)
    n += 1
    if n == 5:
        break