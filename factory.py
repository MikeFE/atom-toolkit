#!/usr/bin/env python3

"""
This factory will create AtoM Toolkit model objects. The factory is primarily
used for getting large numbers of objects at once or for building model objects
from SQLAlchemy query results.
"""

import logging
import inflection

import utils

from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_, tuple_

from model.object import Object
from model.object_i18n import ObjectI18n
from model.information_object import InformationObject

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class ObjectFactory:
    @staticmethod
    def build(db, class_name, values):
        """ Builds an object of type cls

        :param db: the database manager.
        :param class_name: the type of object to create
        :param values: initial values for the object to have, this should be a row from 
        the result of an alchemy query
        """

        if len(values) == 0:
            raise Exception('Invalid values given to ObjectFactory!')

        cls_camelized = inflection.camelize(class_name)
        cls_underscored = inflection.underscore(class_name)

        # We sometimes will enable use_labels in our queries to prevent
        # column naming conflicts; in this situation alchemy will add
        # 'table_name_' as a prefix:
        prefix = cls_underscored + '_' if cls_underscored + '_' in values.keys()[0] else ''

        try:
            if cls_underscored not in db.metadata.tables:
                raise KeyError

            obj = globals()[cls_camelized](db)

        except KeyError as e:
            raise Exception('ObjectFactory does not know how to build a %s' % cls_camelized)

        for col in obj.cols:
            val = utils.result_get(values, prefix + col)
            setattr(obj, col, val)

        if obj.has_i18n():
            if len(prefix) > 0:
                prefix += 'i18n_' # use_labels=True

            # There might be a case where we're parsing a query result
            # on an object that has a corresponding i18n table, but the
            # particular query didn't join with it.
            if utils.result_get(values, prefix + 'culture') is not None:
                cul = values[prefix + 'culture']
                obj.add_culture(cul)

                for col in obj.cols_i18n:
                    val = utils.result_get(values, prefix + col)
                    setattr(getattr(obj, cul), col, val)

        return obj

    @staticmethod
    def get_by_ids(db, class_name, ids, culture='en'):
        """ Fetches multiple objects at once, this method is a generator

        :param class_name: the type of object to grab, e.g. 'actor'.

        :param ids: a list of the ids to fetch. An empty list means get all 
        objects of this type.

        :param culture: is which i18n culture to hydrate. If you need to 
        get all the i18n values for all available cultures, use hydrate instead.
        This method is meant for getting many info objects quickly, not be
        thorough.
        """

        table_name = inflection.underscore(class_name)
        obj = db.table(table_name)

        # Check if there's an i18n to go along with specified culture
        if table_name + '_i18n' in db.metadata.tables:
            obj_i18n = db.table(table_name + '_i18n')

            sql = select([obj, obj_i18n], use_labels=True).where(
                and_(
                    obj.c.id == obj_i18n.c.id, 
                    obj_i18n.c.culture == culture,
                    obj.c.id.in_(ids)
                )
            )
        else:
            sql = select([obj]).where(obj.c.id.in_(ids))

        result = db.conn.execute(sql)
        rows = result.fetchall()

        for row in rows:
            yield ObjectFactory.build(db, class_name, row)