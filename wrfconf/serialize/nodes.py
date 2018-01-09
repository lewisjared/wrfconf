class Node(object):
    def __init__(self, tag, value, start_mark, end_mark):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        return self.value


class ScalarNode(Node):
    id = 'scalar'

    def __init__(self, tag, value, start_mark=None, end_mark=None):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark



class CollectionNode(Node):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


class SectionNode(CollectionNode):
    id = 'section'


class SequenceNode(CollectionNode):
    id = 'sequence'
    end_mark = ','


class KeyValueNode(CollectionNode):
    id = 'keyvalue'
