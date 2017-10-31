from unittest import TestCase
from ..core.Workshop import Workshop
from ..core.ProductionLine import Flex

class WorkshopTestCase(TestCase):
    def setUp(self):
        self.workshop = Workshop(capacity=4, status='buy')

    def tearDown(self):
        del self.workshop

    def test_sell_line(self):
        line1 = Flex(product_type='p1')
        line2 = Flex(product_type='p2')
        for _ in range(3):
            line1.construct()
            line2.construct()
        self.workshop.add_line(line1, slot_id=1)
        self.workshop.add_line(line2, slot_id=2)
        # 现在厂房里面是有两条生产线的
        print(self.workshop.lines)
        self.assertEqual(self.workshop[1], line1)
        self.assertEqual(self.workshop[2], line2)
        # 卖掉一个
        self.workshop.sell_line(slot_id=1)
        print(self.workshop.lines)
        self.assertEqual(self.workshop[2], line2)
