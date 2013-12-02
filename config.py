#!/usr/bin/env python3

"""
This class manages the AtoM Toolkit JSON configuration file.
"""

import json
import logging

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class Config:
    def __init__(self, file_path):
        """ Opens the config file

        This method will log any exceptions that occur.
        """
        self.file_path = file_path

        try:
            with open(file_path, 'r') as f:
                self.values = json.load(f)
        except IOError as e:
            logging.critical('Error opening config file %s: %s' % (file_path, str(e)))
            raise
        except:
            logging.critical('Error parsing JSON for config file %s' % file_path)
            raise

    def save(self):
        """ Saves the config file

        This method will log any exceptions that occur.
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.values, f)
        except IOError as e:
            logging.error('Error writing config file %s: %s' % (file_path, str(e)))
            raise
        except:
            logging.error('Error writing JSON for config file %s' % file_path)
            raise

    def __str__(self):
        return json.dumps(self.values, sort_keys=True, indent=4)

    def __getitem__(self, k):
        return self.values[k]

    def __setitem__(self, k, v):
        self.values[k] = v
