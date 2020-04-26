import sys
import argparse
import logging
from model import Model

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def main(parser):

    (Model()).run(parser)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='JobXplainer - Diagnóstico de performance para scripts Hive SQL.')
    parser.add_argument('-f', '--file', dest='sql_file', default='xplain_this.sql', help='Aceita caminho para um arquivo SQL (default: /path/to/file/xplain_this.sql)')
    parser.add_argument('-d', '--directory', dest='sql_dir', default='sql_scripts/', help='(default: /path/to/directory/sql_scripts/)')
    
    if not len(sys.argv) > 1:
        print((parser.parse_args()).sql_file)
        logging.info('Você não acionou nenhum parâmetro. Execute --help para saber opções. Execução padrão iniciada.')
        main(parser)
    else:
        print((parser.parse_args()).sql_scripts())
        main(parser)



