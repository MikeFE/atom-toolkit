#!/usr/bin/env python3

"""
This class represents an InformationObject in AtoM.
"""

import logging
import utils

from model.object import *

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class InformationObject(Object): 
    def __init__(self, db):
        super().__init__(db)
        self.cols_i18n = utils.get_col_names(db.table(self.table_name + '_i18n'))