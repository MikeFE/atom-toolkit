#!/usr/bin/env python3

"""
Some generic helper functions for AtoM Toolkit.
"""

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

def get_col_names(table_metadata):
    """ Returns the column names in a table's meta-data """
    return [str(col).split('.')[-1] for col in table_metadata.c]

def result_get(result, column_name, default=None):
    """ Returns column in result, else default if not found

    SQLAlchemy query results don't implement the .get() method
    but can act as dictionaries otherwise. This method acts like
    .get() would on a dict.

    :param result: SQLAlchemy query result 
    :param column_name: the name of the column to get from the result
    :param default: the default value if the column isn't in the result
    """

    return result[column_name] if column_name in result.keys() else default