import os
import sys
import logging
import yaml
import getpass
from datetime import datetime


class Settings:


    def __init__(self, root_file=__file__):

        self.ROOT_DIR = os.path.dirname(os.path.abspath(root_file))
        self.CONFIG_PATH = os.path.join(
            os.path.abspath(os.path.join(self.ROOT_DIR, os.pardir)),
            'resources')
        self.LOG_DIR = os.path.join(
            os.path.abspath(os.path.join(self.ROOT_DIR, os.pardir)), 'LOGS')


class LogStream:


    settings = Settings()


    def __init__(self, specify_log_path=False, settings=settings):


        self.specify_log_path = specify_log_path
        self.log_dir = settings.LOG_DIR


    def log_stream(self, origin, to_file=True, _log_dir=settings.LOG_DIR):


        log = logging.getLogger(origin)
        log.setLevel(logging.DEBUG)

        if to_file:

            if not os.path.isdir(_log_dir):

                os.makedirs(_log_dir)

            handler = logging.FileHandler(os.path.join(_log_dir, '{}_jobXplainer_{}.log'.format(origin, ((datetime.now()).strftime('%Y_%m_%d_%Hh%Mm%Ss')))))

        else:

            handler = logging.StreamHandler(sys.stdout)

        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        if log.hasHandlers():
            
            log.info('Logging Handler para {} encontrado!'.format(origin))

        else: 

            log.info('Logging Handler para {} não encontrado. Novo handler adicionado!'.format(origin))
        
        return log


    def root_logger(self, silent_logger='yes', _log_dir=settings.LOG_DIR):


        if not os.path.isdir(_log_dir):

            os.makedirs(_log_dir)

        if silent_logger == 'no': 
            
            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            handler = logging.FileHandler(os.path.join(_log_dir, 'All_jobXplainer_{}.log'.format((datetime.now()).strftime('%Y_%m_%d_%Hh%Mm%Ss'))))
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
            root.info('Logging Handler para stdout_jobXplainer adicionado!')

        elif silent_logger == 'yes':
        
            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            handler = logging.FileHandler(os.path.join(_log_dir, 'All_jobXplainer_{}.log'.format((datetime.now()).strftime('%Y_%m_%d_%Hh%Mm%Ss'))))
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
            root.info('Logging Handler para All_jobXplainer adicionado!')
            
            return root

        elif silent_logger not in ('no', 'yes'):

            root.error('Argumento -s "{}" não existe.'.format(silent_logger))
            raise AttributeError('Argumento -s "{}" não existe.'.format(silent_logger))


class Configuration:


    def load_config(self, path_config):

        _logstream = LogStream()
        log = _logstream.log_stream(origin=__class__.__name__)
        dir_ls = list(os.scandir(path_config))
        dir_ls.sort(key=os.path.getctime, reverse=True)

        _path_config_file = [
            file.name for file in dir_ls if file.name == 'jobXplainer.yaml'
        ]

        if len(_path_config_file) > 1:

            log.error('Mais de um arquivo jobXplainer.yaml foi identificado. Confira os arquivos em {}'.format(path_config))
            raise AttributeError('Mais de um .yaml encontrado em {}'.format(path_config))

        elif len(_path_config_file) < 1:

            log.error('Nenhum arquivo de configuração jobXplainer.yaml encontrado. Confira em {}'.format(path_config))
            raise AttributeError('Nenhum .yaml encontrado em {}'.format(path_config))

        log.info('Carregando arquivo de configuration.')
        path_config_file = os.path.join(path_config, _path_config_file[0])

        try:

            with open(path_config_file, 'rb') as yml:

                config = yaml.safe_load(yml)

        except IOError as e:

            log.error('Carregamento de arquivo yaml falhou. Confira em ' +
                      path_config,
                      exec_info=True)

            raise(e)

        log.info('Arquivo de configuration carregado.')

        return config


class Security:


    def __init__(self):

        settings = Settings()
        configuration = Configuration()
        config = configuration.load_config(settings.CONFIG_PATH)
        ktb_path = config['profile']['kerberos']['keytab']
        self.ktb_path = ktb_path.format(username=getpass.getuser())

    def kbrs_auth(self):

        pass

    def set_kinit(self, ktb_path):

        pass
