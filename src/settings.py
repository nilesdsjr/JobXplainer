import os
import sys
import logging
from datetime import datetime


class Settings:

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')


class LogStream:

    settings = Settings()

    def log_stream(self, origin, to_file=True, ROOT_DIR=settings.ROOT_DIR):

        root = logging.getLogger(origin)
        root.setLevel(logging.DEBUG)
        if to_file:

            log_dir = os.path.join(os.path.abspath(os.path.join(ROOT_DIR, os.pardir)), 'LOGS')
            print(log_dir)
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)
            handler = logging.FileHandler(os.path.join(log_dir, origin +'_jobXplainer_' +((datetime.now()).strftime('%Y_%m_%d_%Hh%Mm%Ss')) + '.log'))
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        return root
