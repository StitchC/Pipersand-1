from unittest import TestCase

from ..core.Bill import Receivables

class ReceivablesTestCase(TestCase):
    def setUp(self):
        self.receivables = Receivables()


    def test_add(self):
        self.receivables.add(num=15,period=3)
        self.assertEqual(self.receivables[3], 15)
