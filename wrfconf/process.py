from collections import OrderedDict
from datetime import timedelta
from os.path import join

import yaml

from wrfconf.serialize import dump
from wrfconf.utils import make_list, convert_str_to_dt, convert_dt_to_str, merge_dicts


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def create_wrf_namelist(conf, stream=None):
    wrf_config = OrderedDict()
    run_info = conf['run_info']
    domain = conf['domain']
    start_time = convert_str_to_dt(run_info['start_date'])
    end_time = convert_str_to_dt(run_info['start_date']) + timedelta(hours=run_info['run_hours'])

    # Merge in the time info
    max_dom = run_info['max_dom']
    wrf_config['time_control'] = {
        'run_days': 0,
        'run_hours': run_info['run_hours'],
        'start_year': make_list(start_time.year, max_dom),
        'start_month': make_list(start_time.month, max_dom),
        'start_day': make_list(start_time.day, max_dom),
        'start_hour': make_list(start_time.hour, max_dom),
        'start_minute': make_list(start_time.minute, max_dom),
        'start_second': make_list(start_time.second, max_dom),
        'end_year': make_list(end_time.year, max_dom),
        'end_month': make_list(end_time.month, max_dom),
        'end_day': make_list(end_time.day, max_dom),
        'end_hour': make_list(end_time.hour, max_dom),
        'end_minute': make_list(end_time.minute, max_dom),
        'end_second': make_list(end_time.second, max_dom),
    }

    # Merge in the domain info
    domain_keys_to_copy = ('e_we', 'e_sn', 'dx', 'dy', 'parent_id', 'i_parent_start', 'j_parent_start', 'parent_grid_ratio')

    wrf_config['domains'] = {
        'max_dom': max_dom,
        'grid_id': list(range(1, max_dom + 1)),
        'parent_time_step_ratio': domain['parent_grid_ratio']
    }
    for k in domain_keys_to_copy:
        wrf_config['domains'][k] = domain[k]

    return dump(merge_dicts(wrf_config, conf['namelist']), stream)


def create_wps_namelist(conf, stream=None):
    wrf_config = OrderedDict()
    run_info = conf['run_info']
    domain = conf['domain']
    end_time = convert_str_to_dt(run_info['start_date']) + timedelta(hours=run_info['run_hours'])

    # Merge in the time info
    max_dom = run_info['max_dom']
    wrf_config['share'] = {
        'max_dom': max_dom,
        'start_date': make_list(run_info['start_date'], max_dom),
        'end_date': make_list(convert_dt_to_str(end_time), max_dom),
    }

    # Merge in the domain info
    domain_keys_to_copy = ('e_we', 'e_sn', 'parent_id', 'parent_grid_ratio', 'i_parent_start', 'j_parent_start', 'ref_lat', 'ref_lon',
                           'ref_x', 'ref_y', 'truelat1', 'truelat2', 'stand_lon', 'geog_data_res')
    wrf_config['geogrid'] = {}
    wrf_config['geogrid']['dx'] = domain['dx'][0]
    wrf_config['geogrid']['dy'] = domain['dy'][0]
    for k in domain_keys_to_copy:
        if k in domain:
            wrf_config['geogrid'][k] = domain[k]

    return dump(merge_dicts(wrf_config, conf['wps']), stream)


def process_conf_file(conf_file, wrf_dir, wps_dir):
    try:
        with open(conf_file) as fh:
            conf = ordered_load(fh, yaml.SafeLoader)
    except IOError as e:
        raise Exception('Could not open file: {}'.format(conf_file))

    create_wrf_namelist(conf, open(join(wrf_dir, 'namelist.input'), 'w'))
    create_wps_namelist(conf, open(join(wps_dir, 'namelist.wps'), 'w'))
