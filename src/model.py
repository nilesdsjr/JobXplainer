import logging
import os
import re
from datetime import datetime
from settings import Settings, LogStream, Configuration


class Model:

    settings = Settings()
    sql_file = settings.ROOT_DIR
    sql_dir = settings.CONFIG_PATH
    _log_stream = LogStream()
    log = _log_stream.log_stream(origin=__name__)
    log.info('Mensagem do model :)')
    _config = Configuration()
    config = _config.load_config(path_config=settings.CONFIG_PATH)

    print(config['profile']['hive']['jdbc']['database'])
    print(config['profile']['hive']['jdbc']['driver'])
    print(config['profile']['hive']['jdbc']['server'])
    print(config['profile']['hive']['jdbc']['principal'])
    print(config['profile']['hive']['jdbc']['port'])

    def __init__(self, sql_file=sql_file, sql_dir=sql_dir):

        self.sql_file = sql_file
        self.sql_dir = sql_dir

    def get_sql_dir(self):

        pass

    def get_sql_files(self, path_sql_dir=sql_dir):

        _dir_ls = os.scandir(path_sql_dir)
        dir_ls = []
        for path in list(_dir_ls):
            dir_ls.append(os.path.join(path_sql_dir, path.name))

        dir_ls.sort(key=os.path.getctime)
        path_sql_files = [
            file for file in dir_ls if re.search(".sql$", file, re.IGNORECASE)
        ]

        return path_sql_files

    def get_query(self, sql_file):

        with open(sql_file, 'r') as f:

            sql = f.read()

        return sql

    def get_explain(self):

        pass

    def get_response(self):

        pass

    def run(self, parser):

        pass

    def run_query(self, sql, cursor):

        sql = "select * from item limit 10"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
