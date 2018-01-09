import yaml
from .serialize import dump

def create_namelists(conf_file, wrf_dir, wps_dir):
    try:
        with open(conf_file) as fh:
            conf = yaml.load(fh)
    except IOError as e:
        raise Exception('Could not open file: {}'.format(conf_file))

    res = dump(conf['namelist'])
    print(res)
