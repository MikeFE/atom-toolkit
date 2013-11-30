"""
This module contains the database interface for AtoM Toolkit
"""

import sqlalchemy
import logging
import sys

__author__ = 'Mike Gale'
__email__ = 'mikeg@artefactual.com'

class DatabaseManager:
    def __init__(self, cfg):
        """ Construct """

        self.cfg = cfg
        self.metadata = None
        self.conn = None

    def get_connection(self):
        """ Connects to the database 

        Uses reflection to build table meta-data.
        Returns a new sqlalchemy.engine.Connection object.
        """

        conn_params = sqlalchemy.engine.url.URL(
            drivername='mysql+pymysql',
            username=self.cfg['db_user'],
            password=self.cfg['db_pass'] if len(self.cfg['db_pass']) > 0 else None,
            host=self.cfg['db_host'],
            port=self.cfg['db_port'],
            database=self.cfg['db_name']
        )

        try:
            self.engine = sqlalchemy.create_engine(conn_params)
            connection = self.engine.connect()

            # Use reflection to get Table meta-data:
            self.metadata = sqlalchemy.schema.MetaData()
            self.metadata.reflect(bind=connection)
        except Exception as e:
            logging.critical('Failed to connect to database %s:%d -- %s' % \
                            (self.cfg['db_host'], self.cfg['db_port'], e))
            sys.exit(1)

        self.conn = connection
        return connection

    def table(self, name):
        """ Shortcut: Returns table meta-data """
        return self.metadata.tables[name]