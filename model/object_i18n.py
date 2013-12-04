#!/usr/bin/env python3

"""
This class represents an Object that also has i18n columns
"""

import logging

import utils
import inflection

from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_

from model.object import *

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class ValuesI18n:
    pass

class ObjectI18n(Object):
    def __init__(self, db, default_culture='en'):
        """ Build the object and get i18n column names """
        super().__init__(db)

        # Add I18n column names-
        self.cols_i18n = utils.get_col_names(db.table(self.table_name + '_i18n'))
        self.default_culture = default_culture
        self.has_cultures = set()

        print('i18n table %s' % self.table_name)

    def get_str(self, all_variables=False):
        """ Add I18n info to Object.get_str() 

        :param all_variables: whether or not to print all variable even if they are None
        """
        s = super().get_str(all_variables)

        for culture in self.has_cultures:
            cul_vals = getattr(self, culture)
            s += '\n\n\t[culture: %s]' % culture

            for col in self.cols_i18n:
                if col == 'id':
                    continue

                val = getattr(cul_vals, col, None)

                if val is None and all_variables == False:
                    continue

                if isinstance(val, str):
                    val = val[:77] + '...' if len(val) > 80 else val

                s += '\n\t - %s => %.80s' % (col, val)

        return s

    def hydrate(self, id=None):
        """ This method gets the object's i18n values from the db 

        :param id: the id of the object to hydrate, otherwise use self.id
        """

        # Hydrate non-I18n columns first:
        id = super().hydrate(id)

        obj_i18n = self.db.table(self.table_name + '_i18n')

        sql = select([obj_i18n]).where(obj_i18n.c.id == id)
        result = self.db.conn.execute(sql)
        rows = result.fetchall()

        for row in rows:
            cul = row['culture']

            self.add_culture(cul)
            for col in self.cols_i18n:
                setattr(getattr(self, cul), col, row[col])

    def add_culture(self, cul):
        """ Adds a culture if it doesn't exist, otherwise does nothing """

        if not hasattr(self, cul):
            self.has_cultures.add(cul)
            setattr(self, cul, ValuesI18n())