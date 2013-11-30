#!/usr/bin/env python3

"""
This class represents an Object in AtoM.
"""

import logging

import utils
import inflection

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

    def hydrate(self, values, use_labels=True):
        """ This method sets the object's values all at once

        This method is used by the factories and certain
        static methods to hydrate the object. Values will
        be a row returned by an alchemy query.

        If use_labels is set that means the table name is prefixed
        to the column name.
        """

        for col in self.cols:
            col_prefixed = self.table_name + '_' + col
            self.__dict__[col] = values[col_prefixed if use_labels else col]

        for col in self.cols_i18n:
            col_prefixed = self.table_name + '_i18n_' + col
            self.__dict__[col] = values[col_prefixed if use_labels else col]

    def __repr__(self):
        s = "<%s" % self.table_name
        if 'id' in self.__dict__:
            s += '(id => %d)' % self.id

        return s + '>'

    def __str__(self):
        s = '[%s]' % self.table_name
        all_cols = set(self.cols + self.cols_i18n)
        for col in all_cols:
            val = str(self.__dict__[col]) if col in self.__dict__ else 'None'
            s += '\n\t%s => %s' % (col, val)

        return s