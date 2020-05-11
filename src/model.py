import logging
import os
import re
from datetime import datetime
from settings import LogStream
from connections import HiveClient


class ModelJobxplainer:


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
                raise AttributeError('Extensão do arquivo {} não reconhecida. Apenas .sql ou .SQL são aceitos.'.format(path_file))

        else:
            self.log.error('{} não existe. Este arquivo é default quando nenhum outro arquivo ou diretório é passado. Crie o arquivo com query ou indique o caminho para um arquivo ou diretório com arquivos sql.'.format(path_file))
            raise AttributeError('{} não existe.'.format(path_file))


    def get_sql_dir(self):


        path_dir = self.opt['sql_metadata']['path_dir']
        self.log.info('Iniciando busca por arquivos sql em {}'.format(path_dir))

        if os.path.exists(path_dir) and os.path.isdir(path_dir):

            if not os.listdir(path_dir):

                self.log.error("Diretório para arquivos sql está vazio. Indique o diretório correto e reinicie o jobXplainer.")
                raise AttributeError('Diretório para arquivos sql está vazio.')

            else:
                _dir_ls = os.scandir(path_dir)
                dir_ls = [(os.path.join(path_dir, path.name)) for path in list(_dir_ls)]
                dir_ls.sort(key=os.path.getctime, reverse=True)
                path_sql_files = [file for file in dir_ls if re.search(".sql$", file, re.IGNORECASE)]

                if len(path_sql_files) < 1:

                    self.log.error("Diretório não possui arquivos sql. Indique o diretório correto e reinicie o jobXplainer.")
                    raise AttributeError('Diretório não possui arquivos sql.')                

                return path_sql_files

        else:
            self.log.error("Diretório para arquivos sql não existe. Indique o diretório correto e reinicie o jobXplainer.")
            raise AttributeError('Diretório para arquivos sql não existe.')


    def get_queries(self, sql_file):
        

        try:

            with open(sql_file, 'r') as f:
                big_string = f.read()
            f.close()

        except IOError('Erro crítico ao tentar abrir arquivo sql.') as io:

            self.log.error('Erro crítico ao tentar abrir arquivo sql.', exec_info=True)
            raise io
        
        if not big_string:

            self.log.warning('Arquivo {} está vazio.'.format(sql_file))
            return big_string


        queries_out = {}
        expression = "(SELECT(.*);)"
        clean_string = ' '.join(big_string.splitlines())
        d = ';'
        queries =  [e+d for e in clean_string.split(d) if e]
        clean_queries = {count:query for count, query in enumerate(queries)}


        
        for id, query in clean_queries.items():

            result = re.search(expression, query, re.IGNORECASE)
            
            if result:
                
                queries_out[id] = {
                    'query' : query,
                    'explainable' : result.group(1)
                }
        
        return queries_out
    


    def save_response(self):


        pass


    def get_explain(self, sqls):


        hive = HiveClient()
        for key in sqls.keys():

            _sqls = dict(sqls[key]['all_queries'])
            
            for key in _sqls.keys():

                _explainable = _sqls[key]['explainable']
                result = hive.execute(_explainable)

        return result


    def _exec_file(self):


        sql_file = self.get_sql_file()
        sql = self.get_queries(sql_file)
        _xplain = self.get_explain(sql)

        return _xplain

    
    def _exec_dir(self):


        sql_dir = self.get_sql_dir()
        sqls = {}

        for count, sql_file in enumerate(sql_dir):

            sqls[count] = {
                'sql_file' : sql_file,
                'all_queries': self.get_queries(sql_file)
                } 

        _xplain = {key:self.get_explain(sqls) for key, value in sqls.items() if value['all_queries']}

        return _xplain


    def run(self):
        

        sql_exe_type = self.opt['sql_metadata']['exec_type']
        

        if sql_exe_type == 'default':

            try:

                xplain = self._exec_file()

            except:

                self.log.warning('Nenhum arquivo xplain_this.sql encontrado. Tentando diretório sql_scripts/.')

            try:

                xplain = self._exec_dir()

            except Exception as e:

                self.log.error('Execução Default sem dados de entrada. Você precisa fornecer algum script sql.', exc_info=True)
                
                raise e

        elif sql_exe_type == 'file':

                xplain = self._exec_file()

        elif sql_exe_type == 'dir':
                
                xplain = self._exec_dir()