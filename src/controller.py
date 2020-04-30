import sys
import argparse
import logging
from model import Model
from settings import LogStream


def main(parser):

    model = Model()
    model.run(parser)

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
        'Aceita caminho para um arquivo SQL, exemplo: /path/to/file/xplain_this.sql (default: ./xplain_this.sql)'
    )

    parser.add_argument(
        '-d',
        '--directory',
        dest='sql_dir',
        default='sql_scripts/',
        help=
        'Caminho para diretório com arquivos SQL, exemplo: /path/to/directory/sql_scripts/ (default: ./sql_scripts/)'
    )

    parser.add_argument(
        '-s',
        '--silent',
        dest='silent_logger',
        default=False,
        help=
        'Visualizar também em linha de comando ou log silencioso para arquivo. True ou False. (default: False)'
    )

    parser.add_argument(
        '-log',
        dest='log_dir',
        default='LOG_DIR',
        help=
        'Pasta destino dos arquivos de LOG. (default: ./LOGS/)'
    )    

    p =parser.parse_args()
    _log_stream = LogStream()

    if p.log_dir == 'ROOT_DIR':

        root_log = _log_stream.root_logger(silent_logger=p.silent_logger)

    else:

        root_log = _log_stream.root_logger(silent_logger=p.silent_logger, _log_dir=p.log_dir)

    if not len(sys.argv) > 1:
        root_log.info((parser.parse_args()).sql_file)
        root_log.info(
            'Controller - Você não acionou nenhum parâmetro. Execute --help para saber opções. Execução padrão iniciada.'
        )
        main(parser)
        root_log.info('Controller - mensagem final')
    else:
        root_log.info((parser.parse_args()).sql_dir)
        main(parser)
