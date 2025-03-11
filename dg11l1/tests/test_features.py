import unittest

import dg11l1.features as features


class TestValidation(unittest.TestCase):

    def test_validate_ifeel_in_range(self):
        for ifeel_temp in range(37):
            features.validate_parameters(ifeel_temp=20)

    def test_validate_ifeel_negative(self):
        with self.assertRaises(ValueError):
            features.validate_parameters(ifeel_temp=-1)

    def test_validate_ifeel_over_range(self):
        with self.assertRaises(ValueError):
            features.validate_parameters(ifeel_temp=37)

