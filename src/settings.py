import os
import sys
import logging
import yaml
from datetime import datetime


class Settings:
    def __init__(self, root_file=__file__):

        self.ROOT_DIR = os.path.dirname(os.path.abspath(root_file))
        self.CONFIG_PATH = os.path.join(
            os.path.abspath(os.path.join(self.ROOT_DIR, os.pardir)),
            'resources')

    def set_kinit(self):

        pass


class LogStream:

    settings = Settings()

    def log_stream(self, origin, to_file=True, ROOT_DIR=settings.ROOT_DIR):

        root = logging.getLogger(origin)
        root.setLevel(logging.DEBUG)

        if to_file:
            log_dir = os.path.join(
                os.path.abspath(os.path.join(ROOT_DIR, os.pardir)), 'LOGS')

            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)

            handler = logging.FileHandler(
                os.path.join(
                    log_dir, origin + '_jobXplainer_' +
                    ((datetime.now()).strftime('%Y_%m_%d_%Hh%Mm%Ss')) +
                    '.log'))

        else:
            handler = logging.StreamHandler(sys.stdout)

        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        root.info('Logging Handler para ' + origin + ' adicionado!')

        return root


class Configuration:
    def load_config(self, path_config):

        _logstream = LogStream()
        log = _logstream.log_stream(origin=__name__)
        dir_ls = list(os.scandir(path_config))
        dir_ls.sort(key=os.path.getctime, reverse=True)

        _path_config_file = [
            file.name for file in dir_ls if file.name == 'jobXplainer.yaml'
        ]

        if len(_path_config_file) > 1:
            log.error(
                'Mais de um arquivo jobXplainer.yaml foi identificado. \n Confira os arquivos em '
                + path_config)
            exit()

        elif len(_path_config_file) < 1:
            log.error(
                'Nenhum arquivo de configuração jobXplainer.yaml encontrado.\n Confira em '
                + path_config)
            exit()

        log.info('Carregando arquivo de configuration.')
        path_config_file = os.path.join(path_config, _path_config_file[0])

        try:

            with open(path_config_file, 'rb') as yml:

                config = yaml.safe_load(yml)

        except Exception as e:

            log.error('Carregamento de arquivo yaml falhou. Confira em ' +
                      path_config,
                      exec_info=True)

            raise (e)

        log.info('Arquivo de configuration carregado.')

        return config
