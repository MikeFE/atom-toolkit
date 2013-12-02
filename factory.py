#!/usr/bin/env python3

"""
This factory will create AtoM Toolkit model objects.
"""

import logging
import inflection

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

        # Accept underscored naming convention as well..
        if class_name.find('_') != -1:
            class_name = inflection.camelize(class_name)

        obj = globals()[class_name](db)


        for col in obj.cols:
            val = values['information_object_' + col] if 'information_object_' +col in values else None
            setattr(obj, col, val)

        return obj

    @staticmethod
    def get_by_ids(db, class_name, ids, culture='en'):
        """ Fetches multiple objects at once

        :param ids: a list of the ids to fetch. An empty list means get all 
        objects of this type.

        :param culture: is which i18n culture to hydrate. If you need to 
        get all the i18n values for all available cultures, use hydrate instead.
        This method is meant for getting many info objects quickly, not be
        thorough.
        """

        table_name = inflection.underscore(class_name)
        obj = db.table(table_name)
        obj_i18n = db.table(table_name + '_i18n')

        sql = select([obj, obj_i18n], use_labels=True).where(
            and_(
                obj.c.id == obj_i18n.c.id, 
                obj_i18n.c.culture == culture,
                obj.c.id.in_(ids)
            )
        )

        result = db.conn.execute(sql)
        rows = result.fetchall()

        for row in rows:
            yield ObjectFactory.build(db, class_name, row)