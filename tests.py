#!/usr/bin/env python3
"""
Quick and dirty tests for AtoM Toolkit development
"""

import config
import sys
import db

from model.object import *
from model.information_object import *
from model.repository import *
from factory import *
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_

cfg = config.Config('./config.json')

dbman = db.DatabaseManager(cfg)

c = dbman.get_connection()

io = dbman.table('information_object')
ioi = dbman.table('information_object_i18n')

sql = select([io, ioi], use_labels=True).where(
                and_(
                    io.c.repository_id != None,
                    io.c.id == ioi.c.id
                )
            ).limit(1)

result = c.execute(sql)
io_with_repo = ObjectFactory.build(dbman, 'information_object', result.fetchone())

print(io_with_repo)

repo = Repository(dbman)
repo.hydrate(id=io_with_repo.repository_id)

print(repo)