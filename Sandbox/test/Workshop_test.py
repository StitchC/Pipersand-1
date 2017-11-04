from unittest import TestCase
from ..core.Workshop import Workshop
from ..core.ProductionLine import Flex

class WorkshopTestCase(TestCase):
    def setUp(self):
        self.workshop = Workshop(capacity=4, workshop_type='medium', status='buy')

    def tearDown(self):
        del self.workshop

    def test_get_rental_cost(self):
        # 小厂房租金3,中4,大5，买回来的0
        workshop1 = Workshop(capacity=3, workshop_type='small', status='rent')
        workshop2 = Workshop(capacity=4, workshop_type='medium', status='rent')
        workshop3 = Workshop(capacity=5, workshop_type='big', status='rent')
        workshop = Workshop(capacity=5, workshop_type='big', status='buy')

        workshop1.rent_season = 1
        workshop2.rent_season = 2
        workshop3.rent_season = 3

        # 要交
        self.assertEqual(workshop1.get_rental_cost(season=1), 3)
        self.assertEqual(workshop2.get_rental_cost(2), 4)
        self.assertEqual(workshop3.get_rental_cost(3), 5)

        # 不用交
        self.assertEqual(workshop.get_rental_cost(1), 0)
        self.assertEqual(workshop1.get_rental_cost(2), 0)

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
