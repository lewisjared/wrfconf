__all__ = ['Serializer', 'SerializerError']

from .nodes import *


class SerializerError(Exception):
    pass


class Serializer:
    def __init__(self, stream):
        self.closed = None
        self.stream = stream

    def open(self):
        if self.closed is None:
            self.closed = False
        elif self.closed:
            raise SerializerError("serializer is closed")
        else:
            raise SerializerError("serializer is already opened")

    def close(self):
        if self.closed is None:
            raise SerializerError("serializer is not opened")
        elif not self.closed:
            self.closed = True

    def serialize(self, section_name, node):
        if self.closed is None:
            raise SerializerError("serializer is not opened")
        elif self.closed:
            raise SerializerError("serializer is closed")

        self.emit('&{}\n'.format(section_name))
        self.serialize_node(node)
        self.emit('/\n\n')

    def emit(self, chars):
        if chars is not None:
            self.stream.write(chars)

    def serialize_node(self, node, indent=0):
        if isinstance(node, ScalarNode):
            if indent:
                self.emit(' ' * indent)
            self.emit(node.start_mark)
            self.emit(node.value)
            self.emit(node.end_mark)
        elif isinstance(node, SequenceNode):
            for item in node.value:
                item.start_mark = '\t'
                self.serialize_node(item)
        elif isinstance(node, SectionNode):
            for key, value in node.value:
                self.serialize_node(key, indent=2)
                self.emit(' = ')
                self.serialize_node(value)
                self.emit('\n')
