import os
import sys
import argparse
import logging
from model import ModelJobxplainer
from settings import Settings, LogStream, Configuration


class CliController:

    '''Can only be called with a argparse Object.'''

    def __init__(self, parser):

        
        self.settings = Settings()
        _log_stream = LogStream()
        self.log = _log_stream.log_stream(origin=__class__.__name__)
        self.parser = parser
        p = self.parser.parse_args()       
        self.all_defaults = {key: parser.get_default(key) for key in vars(p)}


    def cli_options(self):

        self.p = self.parser.parse_args()
        default_f = self.all_defaults['sql_file']
        default_d = self.all_defaults['sql_dir']
        default_sql_file = os.path.join(self.settings.CONFIG_PATH, default_f )
        default_sql_dir = os.path.join(self.settings.CONFIG_PATH, default_d )

        if self.p.sql_file == 'xplain_this.sql' and self.p.sql_dir == 'sql_scripts/':
            
            self.sql_file = default_sql_file
            self.sql_dir = default_sql_dir
            self.log.warning('Nenhum parâmetro recebido. Execução default carregada.')
            self.sql_exec = 'default'

        elif self.p.sql_file != 'xplain_this.sql' and self.p.sql_dir == 'sql_scripts/':

            self.sql_file = self.p.sql_file
            self.sql_dir = default_sql_dir
            self.log.info('Caminho para arquivo SQL carregado.')
            self.sql_exec = 'file'
        
        elif self.p.sql_file == 'xplain_this.sql' and self.p.sql_dir != 'sql_scripts/':

            self.sql_file = default_sql_file
            self.sql_dir = self.p.sql_dir
            self.log.info('Caminho para diretório SQL carregado.')
            self.sql_exec = 'dir'
        
        elif self.p.sql_file != 'xplain_this.sql' and self.p.sql_dir != 'sql_scripts/':

            self.log.error('Apenas um dos argumentos -f ou -d será aceito.')
            raise AttributeError('Apenas um dos argumentos -f ou -d será aceito.')

        cli_options = {
            'sql_metadata' : {
                'path_file' : self.sql_file,
                'path_dir' : self.sql_dir,
                'exec_type' : self.sql_exec
            },
        }

        return cli_options


def main(parser):


    settings = Settings()
    _config = Configuration()
    config = _config.load_config(path_config=settings.CONFIG_PATH)
    p = parser.parse_args()
    specify_log_path = config['profile']['logging']['specify_log_path']
    path_to_log_dir = config['profile']['logging']['path_to_dir']
    _root_log = LogStream()

    if p.log_dir == 'LOG_DIR' and not specify_log_path:

        log = _root_log.root_logger(silent_logger=p.silent_logger)

    elif p.log_dir == 'LOG_DIR' and specify_log_path:

        log = _root_log.root_logger(silent_logger=p.silent_logger, _log_dir=path_to_log_dir)
        
    elif p.log_dir != 'LOG_DIR' and not specify_log_path:
        
        log = _root_log.root_logger(silent_logger=p.silent_logger, _log_dir=p.log_dir)

    cliController = CliController(parser)
    cli_options = cliController.cli_options()
    
    if not len(sys.argv) > 1: 
        
        log.info('Você não acionou nenhum parâmetro. Execute --help para saber opções. Execução padrão iniciada.')

    model = ModelJobxplainer(cli_options)
    model.run()


if __name__ == '__main__':


    parser = argparse.ArgumentParser(
        description=
        'JobXplainer - Diagnóstico de performance para scripts Hive SQL.'
    )

    parser.add_argument(
        '-f',
        '--file',
        dest='sql_file',
        default='xplain_this.sql',
        help=
        'Aceita caminho para um arquivo SQL, exemplo: /path/to/file/xplain_this.sql (default: resources/xplain_this.sql)'
    )

    parser.add_argument(
        '-d',
        '--directory',
        dest='sql_dir',
        default='sql_scripts/',
        help=
        'Caminho para diretório com arquivos SQL, exemplo: /path/to/directory/sql_scripts/ (default: resources/sql_scripts/)'
    )

    parser.add_argument(
        '-s',
        '--silent',
        dest='silent_logger',
        default='yes',
        help=
        'Log silencioso para arquivo ou exibir na linha de comando. yes ou no. (default: yes)'
    )

    parser.add_argument(
        '-log',
        dest='log_dir',
        default='LOG_DIR',
        help=
        'Pasta destino dos arquivos de LOG. (default: LOGS/)'
    )    

    main(parser)
