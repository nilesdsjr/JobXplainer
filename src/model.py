import logging
import os
import re
from datetime import datetime
from settings import Settings, LogStream, Configuration


class Model:


    def __init__(self, parser, sql_file=sql_file, sql_dir=sql_dir, _log_stream=_log_stream):

        settings = Settings()
        sql_file = settings.ROOT_DIR
        sql_dir = settings.CONFIG_PATH
        _log_stream = LogStream()
        _config = Configuration()
        config = _config.load_config(path_config=settings.CONFIG_PATH)
        self.p = parser

        specify_log_path = config['profile']['logging']['specify_log_path']

        if self.p.log_dir == 'LOG_DIR' and not specify_log_path:
            
            self.log = _log_stream.log_stream(origin=__name__)

        elif self.p.log_dir == 'LOG_DIR' and specify_log_path:

            self.log = _log_stream.log_stream(origin=__name__, _log_dir=config['profile']['logging']['path_to_dir'])
            
        elif self.p.log_dir != 'LOG_DIR' and not specify_log_path:
                
            self.log = _log_stream.log_stream(origin=__name__, _log_dir=self.p.lod_dir)


        if self.p.sql_file == 'xplain_this.sql' and self.p.sql_dir == 'sql_scripts/':
            
            self.sql_file = sql_file
            self.sql_dir = sql_dir

        elif self.p.sql_file != 'xplain_this.sql' and self.p.sql_dir == 'sql_scripts/':

            self.sql_file = self.p.sql_file
            self.sql_dir = sql_dir
            self.log.info('Caminho para arquivo SQL carregado.')
        
        elif self.p.sql_file == 'xplain_this.sql' and self.p.sql_dir != 'sql_scripts/':

            self.sql_file = sql_file
            self.sql_dir = self.p.sql_dir
            self.log.info('Caminho para diretório SQL carregado.')


    

    def get_sql_dir(self):

        pass

    def get_sql_files(self, path_sql_dir=None):

        if path_sql_dir==None: path_sql_dir=self.path_sql_dir

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

        cursor.execute(sql)
        results = cursor.fetchall()

        return results
