#!/usr/bin/env python3

"""
This class represents a Repository in AtoM.
"""

import logging
import utils

from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from model.actor import *

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class Repository(Actor): 
    def __init__(self, db):
        """ 
        :param db: The database manager for this object
        """
        super().__init__(db)