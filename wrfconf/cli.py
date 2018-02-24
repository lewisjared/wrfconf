import argparse

from wrfconf.conf.parse_namelist import process_namelist
from wrfconf.process import process_conf_file

def gen_params_parser(subparsers):
    gen = subparsers.add_parser('gen_params', help='Generate a configuration file containing the valid WRF parameters')
    gen.add_argument('input', help='input README.namelist filename')


def create_parser(subparsers):
    create = subparsers.add_parser('create', help='Create new configuration files for a WRF run')
    create.add_argument('input', help='YML configuration file for the run')
    create.add_argument('-n', '--namelist', default='.', help='Folder to store the WRF namelist file')
    create.add_argument('-w', '--wps', default='.', help='Folder to store the WPS file')


def run_command(args):
    if args.cmd == 'gen_params':
        print(process_namelist(args.input))
    elif args.cmd == 'create':
        process_conf_file(args.input, args.namelist, args.wps)


def main():
    parser = argparse.ArgumentParser(prog='wrfconf',
                                     description="Generate WRF configuration from structured YAML files")
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    create_parser(subparsers)
    gen_params_parser(subparsers)

    args = parser.parse_args()
    run_command(args)


main()