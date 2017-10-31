from unittest import TestCase

from ..core.ProductionCenter import ProductionCenter

class ProductionCenterTestCase(TestCase):
    def setUp(self):
        self.production_center = ProductionCenter()

    def test_buy(self):
        self.production_center.buy(workshop_type='small', slot_id=1)
        print(self.production_center.workshops)
        self.assertEqual(self.production_center[1].status, 'buy')
