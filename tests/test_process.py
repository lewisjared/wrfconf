from unittest import TestCase
from wrfconf.process import create_wrf_namelist, create_wps_namelist, ordered_load
from six import StringIO


class TestWRF(TestCase):
    def setUp(self):
        self.cfg = ordered_load(open('examples/run.yml'))
        with open('examples/namelist.input') as f:
            lines = f.readlines()
        self.expected = ''.join(lines)

    def test_create(self):
        self.assertEqual(create_wrf_namelist(self.cfg), self.expected)

    def test_stream(self):
        stream = StringIO()
        create_wrf_namelist(self.cfg, stream)
        stream.seek(0)
        self.assertEqual(''.join(stream.readlines()), self.expected)


class TestWPS(TestCase):
    def setUp(self):
        self.cfg = ordered_load(open('examples/run.yml'))
        with open('examples/namelist.wps') as f:
            lines = f.readlines()
        self.expected = ''.join(lines)

    def test_create(self):
        self.assertEqual(create_wps_namelist(self.cfg), self.expected)

    def test_stream(self):
        stream = StringIO()
        create_wps_namelist(self.cfg, stream)
        stream.seek(0)
        self.assertEqual(''.join(stream.readlines()), self.expected)