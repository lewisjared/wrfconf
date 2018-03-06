import re
from collections import defaultdict

import yaml

default_parser = re.compile('^[a-z0-9 _()\t]*?=.s*?([0-9\w,<>\'\s]+)[;\(\|]?(.*)$', re.DOTALL)


def is_command(l):
    return is_section_item(l) or default_parser.search(l) is not None


def is_section_item(l):
    try:
        return l.strip()[0] == '&'
    except IndexError:
        return False


class ConfigItem(object):
    def __init__(self, line):
        self.raw = line
        self.name = None
        self.is_multi_dim = False
        self.is_section = False
        self.description = ""
        self.default = None
        self.process(line)

    def __str__(self):
        if self.is_section:
            return '<section {}>'.format(self.name)
        else:
            return '<item {} default={} is_multi_dim={}>'.format(self.name, self.default, self.is_multi_dim)

    def process(self, l):
        if l[0] == '&':
            self.is_section = True
            self.name = l.strip()
            if ' ' in self.name:
                self.name = self.name[:self.name.find(' ')]
            self.name = self.name.strip('&:')
        else:
            raw_name = l[:l.find('=')]
            if '(max_dom)' in raw_name:
                self.is_multi_dim = True
            self.name = raw_name.replace('(max_dom)', '').strip()

            res = default_parser.search(l, )
            if res:
                self.default = res.group(1).strip().strip(',')
                self.description = res.group(2).strip()
                self.description = '\n'.join([a.strip() for a in self.description.split('\n')])
                pass

    def to_dict(self):
        return {
            'name': self.name,
            'default': self.default,
            'description': self.description,
            'is_multi_dim': self.is_multi_dim
        }


def get_next_item(lines):
    """
    Find the next item
    :param lines: List of lines
    :return: The line to process with any newlines removed
    """
    while len(lines):
        l = lines.pop(0)

        # Determine if the line is part of a var or text
        if is_command(l):
            res = l

            # Peek at the next item and see if it is not blank
            while len(lines):
                if lines[0] != "\n" and not is_command(lines[0]):
                    l = lines.pop(0)
                    res += l
                else:
                    break

            return res.strip()


def stringify(items):
    d = {}
    for item in items:
        d[item] = []
        for v in items[item]:
            d[item].append(v.to_dict())
    return yaml.dump(d, default_flow_style=False)


def process_namelist(fname):
    with open(fname) as fh:
        lines = fh.readlines()

    # Store the current section to parse the hierachy
    current_section = None
    items = defaultdict(set)
    while len(lines):
        item_str = get_next_item(lines)
        item = ConfigItem(item_str)

        if item.is_section:
            current_section = item
        else:
            if item.name and item.name not in items[current_section.name]:
                items[current_section.name].add(item)
    # Stringify
    return stringify(items)
