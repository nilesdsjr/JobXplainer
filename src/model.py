import logging
import os
from datetime import datetime
from settings import Settings, LogStream


class Model:

    paths = Settings()
    sql_file = paths.ROOT_DIR
    sql_dir = paths.CONFIG_PATH
    _log_stream = LogStream()
    log = _log_stream.log_stream(origin=__name__)
    log.info('Mensagem do model :)')

    def __init__(self, sql_file=sql_file, sql_dir=sql_dir):

        self.sql_file = sql_file
        self.sql_dir = sql_dir

    def get_sql_dir(self):

        pass

    def get_sql_file(self):
        pass

    def get_query(self):
        pass

    def get_explain(self):
        pass

    def get_response(self):
        pass

    def run(self, parser):
        pass
