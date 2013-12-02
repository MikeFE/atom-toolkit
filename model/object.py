#!/usr/bin/env python3

"""
This class represents an Object in AtoM.
"""

import logging

import utils
import inflection

from sqlalchemy.sql import select

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class Object:
    def __init__(self, db):
        """ Constructs an AtoM Object.

        db should be the DatabaseManager instance this 
        object will use.
        """

        self.db = db
        self.table_name = inflection.underscore(type(self).__name__)
        self.cols = utils.get_col_names(db.table(self.table_name))
        self.cols_i18n = [] # We set these later on in the children

    def get_str(self, all_variables=True):
        """ Returns a string representation of the object

        If all_variables=True, return a string showing all
        col variables, even if they None (may be useful in debugging)
        """
        s = '[%s' % self.table_name
        if hasattr(self, 'id') and self.id is not None:
            s += ', id: %d' % self.id

        s += ']'

        for col in self.cols:
            if col == 'id':
                continue

            val = getattr(self, col, None)
            if val is None and all_variables == False:
                continue

            s += '\n\t%s => %s' % (col, val)

        return s

    def __repr__(self):
        s = "<%s" % self.table_name
        if hasattr(self, 'id'):
            s += '(id => %d)' % self.id

        return s + '>'

    def __str__(self):
        return self.get_str(all_variables=False)

    def hydrate(self, id=None):
        """ This method gets the object's values from the db """

        if id is None and hasattr(self, 'id'):
            id = self.id

        if id is None: 
            raise Exception('object.hydrate() called without a valid id')

        io = self.db.table('information_object')

        sql = select([io]).where(io.c.id == id)
        result = self.db.conn.execute(sql)

        row = result.fetchone()
        if row is None:
            raise Exception('object.hydrate() failed -- no object in the database with id: %d', id)

        for col in self.cols:
            setattr(self, col, row[col])

        return id # We use this in the I18n hydrate()
