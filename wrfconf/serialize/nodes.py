class Node(object):
    def __init__(self, value, start_mark, end_mark):
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        return self.value


class ScalarNode(Node):
    id = 'scalar'

    def __init__(self, value, start_mark=None, end_mark=None):
        super(ScalarNode, self).__init__(value, start_mark, end_mark)


class CollectionNode(Node):
    id = 'collection'

    def __init__(self, value, start_mark=None, end_mark=None):
        super(CollectionNode, self).__init__(value, start_mark, end_mark)


class SectionNode(CollectionNode):
    id = 'section'


class SequenceNode(CollectionNode):
    id = 'sequence'
