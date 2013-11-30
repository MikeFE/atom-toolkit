#!/usr/bin/env python3

"""
Some generic helper functions for AtoM Toolkit.
"""

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

def get_col_names(table_metadata):
    """ Returns the column names in a table's meta-data """
    return [str(col).split('.')[-1] for col in table_metadata.c]