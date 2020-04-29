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

    def __init__(self, sql_file=sql_file, sql_dir=sql_dir, log=log):

        self.sql_file = sql_file
        self.sql_dir = sql_dir
        self.log = log

    def get_sql_dir(self):

        pass

    def get_sql_files(self, path_sql_dir=sql_dir):

        self.log.info('Iniciando busca por arquivos sql em ' + path_sql_dir)

        if os.path.exists(path_sql_dir) and os.path.isdir(path_sql_dir):

            if not os.listdir(path_sql_dir):

                self.log.error(
                    "Diretório para arquivos sql está vazio. Indique o diretório correto e reinicie o jobXplainer."
                )
                raise (ValueError())

            else:

                _dir_ls = os.scandir(path_sql_dir)
                dir_ls = [(os.path.join(path_sql_dir, path.name))
                          for path in list(_dir_ls)]
                dir_ls.sort(key=os.path.getctime, reverse=True)
                path_sql_files = [
                    file for file in dir_ls
                    if re.search(".sql$", file, re.IGNORECASE)
                ]

                return path_sql_files

        else:

            self.log.error(
                "Diretório para arquivos sql não existe. Indique o diretório correto e reinicie o jobXplainer."
            )
            raise (ValueError())

    def get_query(self, sql_file):

        try:

            with open(sql_file, 'r') as f:
                sql = f.read()
            f.close()

        except Exception as e:

            self.log.error('Erro crítico ao tentar abrir arquivo sql.',
                           exec_info=True)
            raise (e)

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
