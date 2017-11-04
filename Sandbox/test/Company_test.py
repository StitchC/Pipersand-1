from unittest import TestCase

from ..core.Company import Company
# from ..core.custom_orders import

class CompanyTest(TestCase):
    def setUp(self):
        self.company = Company()

    def test_new_company_in_initial_state(self):
        self.assertEqual(self.company.expenditures['ISO资格认证'], 0)

    def test_end_season(self):
        # 短期贷款20
        self.company.short_loan(20)

        self.company.end_season()

        # 短期贷款20还有3个季度要还
        self.assertEqual(self.company.short_liability[3], 20)
        self.assertEqual(self.company.season, 2)
        self.fail("还有更新管理费，物流状态那些")

    def test_long_loan(self):
        self.company.long_loan(value=50, year=2)
        self.assertEqual(self.company.long_liability[2], 50)
        # 现金变成60 + 50 = 110
        self.assertEqual(self.company.cash, 110)

    def test_update_long_loan(self):
        # 借的是2年的长期贷款，更新后变成1年期的
        self.company.long_loan(value=50, year=2)
        self.company.update_long_loan()
        self.assertEqual(self.company.long_liability[1], 50)
        self.assertEqual(self.company.long_liability[2], 0)
        # 还利息5，现金变成60 + 50 - 5 = 105
        self.assertEqual(self.company.cash, 105)
        # 所有者权益减少60 - 5 = 55
        self.assertEqual(self.company.equity, 55)

    def test_short_loan(self):
        self.company.short_loan(value=20)
        # 4季的短期贷款有20
        self.assertEqual(self.company.short_liability[4], 20)
        # 现金增加60 + 20 = 80
        self.assertEqual(self.company.cash, 80)
        # 4季后到期的短期贷款有20
        self.assertEqual(self.company.short_liability[4], 20)

    def test_update_short_loan(self):
        self.company.short_loan(value=20)
        # 一季度过后变成还有3季度到期
        self.company.update_short_loan()
        self.assertEqual(self.company.short_liability[4], 0)
        self.assertEqual(self.company.short_liability[3], 20)
        # 再过3个季度，换本付息，现金变成60 + 20 - 21 = 59
        for _ in range(3):
            self.company.update_short_loan()
        self.assertEqual(self.company.cash, 59)
        # 利息是1，所有者权益变成59
        self.assertEqual(self.company.equity, 59)

    def test_order_raw_material(self):
        order = {'r1': 3, 'r2': 2, 'r3': 1, 'r4': 1}
        self.company.order_raw_material(order=order)
        # 查看下一个季度到的原材料，里面有3个r1，2个r2，0个r3，0个r4
        self.assertEqual(self.company.logistic[1]['r1'], 3)
        self.assertEqual(self.company.logistic[1]['r2'], 2)
        self.assertEqual(self.company.logistic[1]['r3'], 0)
        self.assertEqual(self.company.logistic[1]['r4'], 0)
        # 查看还有两个季度到的原材料，里面有0个r1，0个r2，1个r3，1个r4
        self.assertEqual(self.company.logistic[2]['r1'], 0)
        self.assertEqual(self.company.logistic[2]['r2'], 0)
        self.assertEqual(self.company.logistic[2]['r3'], 1)
        self.assertEqual(self.company.logistic[2]['r4'], 1)

    def test_update_raw_material(self):
        order = {'r1': 3, 'r2': 2, 'r3': 1, 'r4': 1}
        self.company.order_raw_material(order=order)
        self.company.update_raw_material()
        # 入库3个r1，2个r2，现金变成60-3-2=55
        self.assertEqual(self.company.cash, 55)
        # 仓库里面有3个r1，2个r2
        self.assertEqual(self.company.store['r1'], 3)
        self.assertEqual(self.company.store['r2'], 2)
        # 还有1个r3和1个r4，1季度之后到
        self.assertEqual(self.company.logistic[1]['r3'], 1)
        self.assertEqual(self.company.logistic[1]['r4'], 1)

    def test_buy_rent_workshops(self):
        # 买大厂房，放在生产中心第一格，大厂房状态是买
        self.company.buy_workshop(workshop_type='big', slot_id=1)
        self.assertEqual(self.company.production_center[1].status, 'buy')
        # 现金是60 - 40 = 20
        self.assertEqual(self.company.cash, 20)
        # 租小厂房
        self.company.rent_workshop(workshop_type='small', slot_id=2)
        self.assertEqual(self.company.production_center[2].status, 'rent')
        # 现金是20 - 3 = 17
        self.assertEqual(self.company.cash, 17)

    """
    已经在很多个地方test了，不过不要删这个testcase，可能有用
    """
    # def test_buy_a_new_line_in_big_workshop(self):
    #     self.company.buy_workshop('big', 1)
    #     self.company.new_line(line_type='Auto', product_type='p1', workshop_id=1, slot_id=1)
    #     # 现金是60 - 40 - 5 = 15
    #     self.assertEqual(self.company.cash, 15)
    #     # 产品类型是'p1'
    #     self.assertEqual(self.company.production_center[1][1].product_type, 'p1')
    #     # 生产线净值是5
    #     self.assertEqual(self.company.production_center[1][1]._net_value, 5)
    #     # 再建了一次这个生产线，现在净值是10
    #     self.company.construct_line(workshop_id=1, line_id=1)
    #     self.assertEqual(self.company.production_center[1][1]._net_value, 10)
    #     # 现金是10
    #     self.assertEqual(self.company.cash, 10)


    def test_sell_line(self):
        self.company.buy_workshop(workshop_type='small', slot_id=1)
        # 买两条生产线
        self.company.new_line(line_type='Flex', product_type='p2', workshop_id=1, slot_id=1)
        self.company.new_line(line_type='Flex', product_type='p2', workshop_id=1, slot_id=2)
        # 两条生产线都建好
        for _ in range(3):
            self.company.construct_line(workshop_id=1, line_id=1)
            self.company.construct_line(workshop_id=1, line_id=2)
            self.assertEqual(len(self.company.constructed_line), 2)
            self.company.end_season()
        # 卖掉第1条，第1条变成None，第2条还在
        self.company.sell_line(workshop_id=1, line_id=1)
        self.assertEqual(self.company.production_center[1][1], None)
        self.assertEqual(self.company.production_center[1][2]._net_value, 20)

    def test_switch_product(self):
        self.company.rent_workshop(workshop_type='small', slot_id=2)
        self.assertEqual(self.company.production_center[2].status, 'rent')

        self.company.buy_workshop(workshop_type='small', slot_id=1)
        self.assertEqual(self.company.production_center[1].status, 'buy')
        # slot_id: 1.手工  2.自动    3.柔性
        # 先把线建起来
        self.company.new_line(line_type='Hand', product_type='p2', workshop_id=1, slot_id=1)
        self.company.new_line(line_type='Auto', product_type='p2', workshop_id=1, slot_id=2)
        self.company.construct_line(workshop_id=1, line_id=2)
        self.company.construct_line(workshop_id=1, line_id=2)
        self.company.new_line(line_type='Flex', product_type='p2', workshop_id=1, slot_id=3)
        self.company.construct_line(workshop_id=1, line_id=3)
        self.company.construct_line(workshop_id=1, line_id=3)
        self.company.construct_line(workshop_id=1, line_id=3)

        # 手工线转产
        self.company.switch_product(workshop_id=1, line_id=1, product_type='p1')
        self.fail("转产过程中不能生产")

    def test_product_dev(self):
        # 研发p1, p2, p3, p4
        self.company.product_dev(['p1','p2','p3','p4'])
        # 现金变成60-1-1-1-2=55
        self.assertEqual(self.company.cash, 55)
        # 费用表的产品研发有5
        self.assertEqual(self.company.expenditures['产品研发'], 5)

    def test_market_dev(self):
        # 开本地，国内，亚洲
        self.company.market_dev(markets=['本地', '国内', '亚洲'])
        # 现金会变成60-3=57
        self.assertEqual(self.company.cash, 57)
        # 费用项目“新市场开拓”是3
        self.assertEqual(self.company.expenditures['新市场开拓'], 3)
        # 本地可以用
        self.assertTrue(self.company.has_certificate(cert='本地'))
        # 国内和亚洲不能用
        self.assertIsNot(self.company.has_certificate(cert='国内'), True)
        self.assertIsNot(self.company.has_certificate(cert='亚洲'), True)
        # 又再开一次国内，现在国内能用
        self.company.market_dev(['国内'])
        self.assertTrue(self.company.has_certificate(cert='国内'))

    def test_iso_dev(self):
        # 开ISO9和14
        self.company.iso_dev(isos=['ISO9', 'ISO14'])
        # 现金变成60-1-2=57
        self.assertEqual(self.company.cash, 57)
        # 费用项目“ISO资格认证”是3
        self.assertEqual(self.company.expenditures['ISO资格认证'], 3)
        # ISO9和14都是2年的，现在不能用
        self.assertIsNot(self.company.has_certificate(cert='ISO9'), True)
        self.assertIsNot(self.company.has_certificate(cert='ISO14'), True)

        # 再开发一次ISO9和14
        self.company.iso_dev(isos=['ISO9', 'ISO14'])
        self.assertTrue(self.company.has_certificate(cert='ISO9'))
        self.assertTrue(self.company.has_certificate(cert='ISO14'))

    def test_get_order_produce_then_delivery(self):
        # 满足拿订单的要求，要有ISO14
        self.company.iso_dev(['ISO14'])
        self.company.iso_dev(['ISO14'])
        # 现金变成60-4=56
        self.assertEqual(self.company.cash, 56)
        # 拿到一张Order('p2', 3, 15, 3, 0, 1, '本地')，3个p2，15块，3交货0账期
        self.company.get_order('test')  # 用来测试的那个订单，id_order['test']
        # 紧急采购3个p2
        self.company.emergency_buy({'p2': 3})
        # 现金变成56-3*9=29
        self.assertEqual(self.company.cash, 29)
        # 提交订单
        self.company.delivery(order_id='test')
        # 现金直接增加15, 29+15=44
        self.assertEqual(self.company.cash, 44)

    def test_discount_receivable(self):
        # 测试交一个不是马上拿到钱的订单
        # Order('p2', 3, 15, 3, 3, 1, 0, market='国内')
        self.company.get_order('test1')
        # 紧急采购3个p2
        self.company.emergency_buy({'p2': 3})
        # cash = 60-3*9=33
        self.assertEqual(self.company.cash, 33)
        # 提交订单
        self.company.delivery(order_id='test1')
        # 现金不变
        self.assertEqual(self.company.cash, 33)
        # 3期应收款多15
        print(self.company.receivables)
        self.assertEqual(self.company.receivables[3], 15)

        # 贴现3期15
        self.company.discount_receiable({3: 15})
        # 财务费用2，现金33 + 13 = 46
        self.assertEqual(self.company.income_statement['财务费用'], 2)
        self.assertEqual(self.company.cash, 46)

    def test_emergency_buy_material(self):
        # 紧急采购5个R1, 3个R3, 1个P1, 3个P3
        items = {'r1': 5, 'r3': 3}
        self.company.emergency_buy(items)
        # 现金变成60-(5*2+3*2)=44
        self.assertEqual(self.company.cash, 44)
        # 仓库里面多了原材料
        inventory = self.company.store.get_inventory()
        self.assertEqual(inventory['r1'], 5)
        self.assertEqual(inventory['r3'], 3)

    def test_emergency_buy_product(self):
        # 紧急采购1个P1, 3个P3
        items = {'p1': 1, 'p3':3}
        self.company.emergency_buy(items)
        # 现金变成60-(1*6+3*15)=18
        self.assertEqual(self.company.cash, 9)
        # 仓库里面多了产品
        inventory = self.company.store.get_inventory()
        self.assertEqual(inventory['p1'], 1)
        self.assertEqual(inventory['p3'], 3)

    def test_auto_produce(self):
        """
        自动线的生产
        """
        # 先建好一条P1的自动线
        self.company.buy_workshop(workshop_type='small', slot_id=1)
        self.company.new_line(line_type='Auto', product_type='p1', workshop_id=1, slot_id=1)
        for _ in range(2):
            self.company.construct_line(workshop_id=1, line_id=1)
            self.company.end_season()

        # 研发P1
        for _ in range(2):
            self.company.product_dev(['p1'])

        # 紧急采购1个r1原料
        self.company.emergency_buy({'r1': 1})

        # 生产一个P1产品，支付1加工费
        self.company.produce(workshop=1, slot_id=1)
        # 现金变成60 - 30 - 15 - 2 - 2 - 1 = 11
        self.assertEqual(self.company.cash, 11)
        # r1原料用掉了
        self.assertEqual(self.company.store['r1'], 0)

    def test_hand_produce(self):
        """
        手工线的生产
        """
        # 先建好一条P1的自动线
        self.company.buy_workshop(workshop_type='small', slot_id=1)
        self.company.new_line(line_type='Hand', product_type='p1', workshop_id=1, slot_id=1)

        # 研发P1
        for _ in range(2):
            self.company.product_dev(['p1'])



    def test_depreciate(self):
        """
        第一季新建3个生产线
        第二季在建两个生产线，当季结束
        第三季在建两个生产线，当季结束
        第四季在建两个生产线，折旧，当季结束
        """
        # 手工线，自动线，柔性线各一条
        # 第一季
        self.company.buy_workshop(workshop_type='small', slot_id=1)
        self.assertEqual(len(self.company.production_center), 1)    # 看看有没有买到厂房
        self.company.new_line(line_type='Hand', product_type='p1', workshop_id=1, slot_id=1)
        self.company.new_line(line_type='Auto', product_type='p1', workshop_id=1, slot_id=2)
        self.company.new_line(line_type='Flex', product_type='p1', workshop_id=1, slot_id=3)

        # 第二第三季
        for _ in range(2):
            self.company.construct_line(workshop_id=1, line_id=2)
            self.company.construct_line(workshop_id=1, line_id=3)
            self.company.end_season()

        # 第四季
        self.company.construct_line(workshop_id=1, line_id=3)

        # 第一年折旧, 手工线，自动线已经建成，但是是新的，不折旧
        self.company.depreciate()
        self.assertEqual(self.company.income_statement['累计折旧'], 0)
        # 第四季结束，第一年结束
        self.company.end_season()
        self.company.end_year()

        # 第二年折旧，手工线折旧1，自动线折旧3，柔性线今年建成，不折旧
        self.company.depreciate()
        self.assertEqual(self.company.income_statement['累计折旧'], 4)

        # 第四季折旧，手工线折旧1，自动线折旧3，柔性线折旧4
        self.company.depreciate()
        self.assertEqual(self.company.income_statement['累计折旧'], 8)


    # def test_
