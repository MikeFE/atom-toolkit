#!/usr/bin/env python3

"""
This class represents a Term in AtoM.
"""

import logging
import utils

from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from model.object_i18n import *

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class Term(ObjectI18n): 
    def __init__(self, db):
        """ 
        :param db: The database manager for this object
        """
        super().__init__(db)