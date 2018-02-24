from datetime import datetime


def merge_dicts(a, b):
    """
    Merge dicts a and b, with values in b overriding a

    Merges at the the second level. i.e. Merges dict top level values
    :return: New dict
    """
    c = a.copy()
    for k in b:
        if k not in c:
            c[k] = b[k]
        else:
            c[k].update(b[k])
    return c


def convert_str_to_dt(s):
    return datetime.strptime(s, '%Y-%m-%d_%H:%M:%S')

def convert_dt_to_str(dt):
    return dt.strftime('%Y-%m-%d_%H:%M:%S')


def make_list(v, num):
    return [v] * num