import warnings
from collections import OrderedDict
from .nodes import ScalarNode, SectionNode, SequenceNode


class RepresenterError(Exception):
    pass


class BaseRepresenter(object):
    wrf_representers = {}

    def represent(self, section_name, data):
        node = self.represent_data(data)
        self.serialize(section_name, node)

    def represent_data(self, data, **kwargs):
        data_types = type(data).__mro__
        if data_types[0] in self.wrf_representers:
            node = self.wrf_representers[data_types[0]](self, data, **kwargs)

            return node

    @classmethod
    def add_representer(cls, data_type, representer):
        if not 'wrf_representers' in cls.__dict__:
            cls.wrf_representers = cls.wrf_representers.copy()
        cls.wrf_representers[data_type] = representer

    def represent_scalar(self, value):
        node = ScalarNode(value, end_mark=',')
        return node

    def represent_sequence(self, sequence, **kwargs):
        value = []
        node = SequenceNode(value)
        for item in sequence:
            node_item = self.represent_data(item, **kwargs)
            value.append(node_item)
        return node

    def represent_section(self, mapping):
        value = []
        node = SectionNode(value)
        if hasattr(mapping, 'items'):
            mapping = list(mapping.items())
            try:
                mapping = sorted(mapping)
            except TypeError:
                pass
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_key.end_mark = None
            node_value = self.represent_data(item_value, is_value=True)
            value.append((node_key, node_value))
        return node


class Representer(BaseRepresenter):

    def represent_str(self, data, is_value=False):
        if ',' in data:
            warnings.warn('Value was potentially incorrectly intepreted as a string, please check: {}'.format(data))
        if is_value:
            return self.represent_scalar("'{}'".format(data))

        return self.represent_scalar(data)

    def represent_bool(self, data, **kwargs):
        if data:
            value = '.true.'
        else:
            value = '.false.'
        return self.represent_scalar(value)

    def represent_int(self, data, **kwargs):
        return self.represent_scalar(str(data))

    inf_value = 1e300
    while repr(inf_value) != repr(inf_value * inf_value):
        inf_value *= inf_value

    def represent_float(self, data, **kwargs):
        if data != data or (data == 0.0 and data == 1.0):
            value = '.nan'
        elif data == self.inf_value:
            value = '.inf'
        elif data == -self.inf_value:
            value = '-.inf'
        else:
            value = repr(data).lower()
            # Note that in some cases `repr(data)` represents a float number
            # without the decimal parts.  For instance:
            #   >>> repr(1e17)
            #   '1e17'
            # Unfortunately, this is not a valid float representation according
            # to the definition of the `!!float` tag.  We fix this by adding
            # '.0' before the 'e' symbol.
            if '.' not in value and 'e' in value:
                value = value.replace('e', '.0e', 1)
        return self.represent_scalar(value)

    def represent_list(self, data, **kwargs):
        # pairs = (len(data) > 0 and isinstance(data, list))
        # if pairs:
        #    for item in data:
        #        if not isinstance(item, tuple) or len(item) != 2:
        #            pairs = False
        #            break
        # if not pairs:
        return self.represent_sequence(data, **kwargs)

    def represent_dict(self, data, **kwargs):
        return self.represent_section(data)


Representer.add_representer(str,
                            Representer.represent_str)

Representer.add_representer(bool,
                            Representer.represent_bool)

Representer.add_representer(int,
                            Representer.represent_int)

Representer.add_representer(float,
                            Representer.represent_float)

Representer.add_representer(list,
                            Representer.represent_list)

Representer.add_representer(tuple,
                            Representer.represent_list)

Representer.add_representer(dict,
                            Representer.represent_dict)

Representer.add_representer(OrderedDict,
                            Representer.represent_dict)