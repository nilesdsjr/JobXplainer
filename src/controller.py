import sys
import argparse
import logging
from model import Model
from settings import LogStream


def main(parser):

    model = Model()
    model.run(parser)


if __name__ == '__main__':

    _log_stream = LogStream()
    log = _log_stream.log_stream(origin=__name__)
    parser = argparse.ArgumentParser(
        description=
        'JobXplainer - Diagnóstico de performance para scripts Hive SQL.')
    parser.add_argument(
        '-f',
        '--file',
        dest='sql_file',
        default='xplain_this.sql',
        help=
        'Aceita caminho para um arquivo SQL (default: /path/to/file/xplain_this.sql)'
    )
    parser.add_argument('-d',
                        '--directory',
                        dest='sql_dir',
                        default='sql_scripts/',
                        help='(default: /path/to/directory/sql_scripts/)')

    if not len(sys.argv) > 1:
        log.info((parser.parse_args()).sql_file)
        log.info(
            'Controller - Você não acionou nenhum parâmetro. Execute --help para saber opções. Execução padrão iniciada.'
        )
        main(parser)
        log.info('Controller - mensagem final')
    else:
        log.info((parser.parse_args()).sql_dir)
        main(parser)
