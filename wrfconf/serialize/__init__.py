from six import StringIO

from .representer import Representer
from .serializer import Serializer


class Dumper(Serializer, Representer):
    def __init__(self, stream):
        Serializer.__init__(self, stream)
        Representer.__init__(self)


def dump(data, stream=None, Dumper=Dumper):
    """
    Serialize Python objects into a WRF namelist stream
    :param data:
    :param stream:
    :return:
    """
    getvalue = None
    if stream is None:
        stream = StringIO()
        getvalue = stream.getvalue

    dumper = Dumper(stream)

    dumper.open()
    for d in data:
        dumper.represent(d, data[d])
    dumper.close()

    if getvalue:
        return getvalue()
