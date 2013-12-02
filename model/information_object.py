#!/usr/bin/env python3

"""
This class represents an InformationObject in AtoM.
"""

import logging
import utils

from model.object_i18n import *

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class InformationObject(ObjectI18n): 
    def __init__(self, db):
        super().__init__(db)
