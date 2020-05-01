import logging
import os
import re
from datetime import datetime
from settings import LogStream

class Model:


    def __init__(self, options):
        

        _log_stream = LogStream()
        self.log = _log_stream.log_stream(origin=__class__.__name__)
        self.opt = options


    def get_sql_file(self):
        

        path_file = self.opt['sql_metadata']['path_file']
        if os.path.isfile(path_file):

            if re.search(".sql$", path_file, re.IGNORECASE):        
                return path_file

            else:
                self.log.error('Extensão do arquivo {} não reconhecida. Apenas .sql ou .SQL são aceitos.'.format(path_file))

        else:
            self.log.error('Dado {} não é um arquivo.'.format(path_file))


    def get_sql_dir(self):


        path_dir = self.opt['sql_metadata']['path_dir']
        self.log.info('Iniciando busca por arquivos sql em {}'.format(path_dir))

        if os.path.exists(path_dir) and os.path.isdir(path_dir):

            if not os.listdir(path_dir):

                self.log.error(
                    "Diretório para arquivos sql está vazio. Indique o diretório correto e reinicie o jobXplainer."
                )

            else:
                _dir_ls = os.scandir(path_dir)
                dir_ls = [(os.path.join(path_dir, path.name)) for path in list(_dir_ls)]
                dir_ls.sort(key=os.path.getctime, reverse=True)
                path_sql_files = [file for file in dir_ls if re.search(".sql$", file, re.IGNORECASE)]

                return path_sql_files

        else:
            self.log.error(
                "Diretório para arquivos sql não existe. Indique o diretório correto e reinicie o jobXplainer."
            )


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

    def save_response(self):

        pass


    def run_query(self, sql, cursor):

        cursor.execute(sql)
        results = cursor.fetchall()

        return results


    def run(self):

        pass