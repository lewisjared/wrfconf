from unittest import TestCase

from wrfconf import ordered_load
from wrfconf.validate import validate_config


class TestValidate(TestCase):
    def setUp(self):
        self.cfg = ordered_load(open('examples/run.yml'))

    def test_full(self):
        is_valid, errors = validate_config(self.cfg)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_invalid(self):
        del self.cfg['domain']['parent_id']
        is_valid, errors = validate_config(self.cfg)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 1)
