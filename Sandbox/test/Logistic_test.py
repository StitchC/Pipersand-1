from unittest import TestCase

from ..core.Logistic import Logistic


class LogisticTest(TestCase):
    def test_can_start_an_empty_Logistic(self):
        logistic = Logistic()
        self.assertEqual(logistic.material_in_transit[0]['r1'], 0)
        self.assertEqual(logistic.material_in_transit[0]['r2'], 0)
        self.assertEqual(logistic.material_in_transit[0]['r3'], 0)
        self.assertEqual(logistic.material_in_transit[0]['r4'], 0)
