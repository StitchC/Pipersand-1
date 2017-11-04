import configparser
config = configparser.ConfigParser()
config.read('C:/Users/67089/Documents/GitHub/Pipersand/Sandbox/core/setting.ini')
CASH = int(config['initial_state']['CASH'])
LOAN_LIMIT_COEFF = int(config['rules']['LOAN_LIMIT_COEFF'])
PRODUCT_DEV_COST = config['product dev cost']
ISO_DEV_COST = config['iso dev cost']
EMERGENCY_BUY_COEF = config['emergency buy coefficient']

MATETIAL_PRICE = config['raw material price']
PRODUCT_PRICE = {}
for product in ['p1', 'p2', 'p3', 'p4']:
    components = product + ' components'
    PRODUCT_PRICE[product] = sum(int(MATETIAL_PRICE[matetial]) * int(num) for
                            matetial, num in config[components].items()) + 1 # +1加工费

WORKSHOP = config['workshop']



from typing import List
import json


from Sandbox.core.Bill import Long_lia, Short_lia, Receivables
from Sandbox.core.Logistic import Logistic
from Sandbox.core.Store import Store
# from Sandbox.core.Workshop import Workshop
from Sandbox.core.ProductionCenter import ProductionCenter
from Sandbox.core.ProductionLine import Hand, Auto, Flex
from Sandbox.core.Order import ObtainOrder
from Sandbox.core.custom_orders import id_order

certificate = {'p1': 2,
               'p2': 4,
               'p3': 6,
               'p4': 6,
               'ISO9': 2,
               'ISO14': 2,
               '本地': 1,
               '区域': 1,
               '国内': 2,
               '亚洲': 3,
               '国际': 4}
expenditures = {'管理费用': 0,
               '广告费': 0,
               '设备维护费': 0,
               '损失': 0,
               '转产费': 0,
               '厂房租金': 0,
               '新市场开拓': 0,
               'ISO资格认证': 0,
               '产品研发': 0,
               '信息费': 0}
balance_sheet = {'现金': 0,
                '应收款': 0,
                '在制品': 0,
                '产成品': 0,
                '原材料': 0,
                '流动资产合计': 0,
                '厂房': 0,
                '生产线': 0,
                '在建工程': 0,
                '固定资产合计': 0,
                '资产总计': 0,
                '长期负债': 0,
                '短期负债': 0,
                '应交所得税': 0,
                '负债合计': 0,
                '股东资本': 0,
                '利润留存': 0,
                '年度净利': 0,
                '所有者权益合计': 0,
                '负债和所有者权益合计': 0}
income_statement = {'销售收入': 0,
                    '直接成本': 0,
                    '毛利': 0,
                    '综合费用': 0,
                    '折旧前利润': 0,
                    '折旧': 0,
                    '支付利息前利润': 0,
                    '财务费用': 0,
                    '税前利润': 0,
                    '所得税': 0,
                    '年度净利润': 0}


class Company(object):
    def __init__(self):
        self.year = 1
        self.season = 1

        self.cash = CASH
        self.long_liability = Long_lia()
        self.short_liability = Short_lia()
        self.receivables = Receivables()

        self.logistic = Logistic()
        self.store = Store()
        self.obtain_order = ObtainOrder()

        self.equity = 60

        self.production_center = ProductionCenter()

        self.certificate = certificate.copy()
        self.expenditures = expenditures.copy()
        self.balance_sheet = balance_sheet.copy()
        self.income_statement = income_statement.copy()

        self.constructed_line = list().copy()

    def reprJSON(self):
        return dict(year=self.year,
                   season=self.season,
                   cash=self.cash,
                   long_liability=self.long_liability,
                   short_liability=self.short_liability,
                   logistic=self.logistic,
                   store=self.store,
                   obtain_order=self.obtain_order,
                   equity=self.equity,
                   production_center=self.production_center,
                   certificate=self.certificate,
                   expenditures=self.expenditures,
                   balance_sheet=self.balance_sheet,
                   income_statement=self.income_statement,
                   constructed_line=self.constructed_line)

    def end_season(self):
        """
        相当于点击当季结束按钮
        """
        if self.season != 4:
            self.season += 1

        # 给1个管理费
        self.expenditures['管理费用'] += 1
        self.cash -= 1

        # 短贷更新
        self.update_short_loan()

        # 之前点了在建的生产线，现在更新
        for _ in range(len(self.constructed_line)):
            line = self.constructed_line.pop()
            line.construct()

        # 物流状态更新
        self.update_raw_material()

    def end_year(self):
        """
        当年结束，计算3个报表，然后清空
        """


        # 清空综合费用表, 利润表
        self.income_statement = income_statement.copy()
        self.expenditures = expenditures.copy()


    def pay_tex(self):
        pass

    def update_long_loan(self):
        """
        更新长期贷款，还本付息
        """
        i, prin = self.long_liability.update()
        self.cash -= i + prin
        self.equity -= i

    def long_loan(self, value: int, year: int) -> None:
        """
        借长期负债
        :param value: 借款额
        :year: 借款时长
        """
        if year not in range(1, 7):
            raise ValueError('借款年限必须是1-6')

        if self.season is not 1:
            raise RuntimeError('不是第一季不能长期贷款')
        if value % 10 != 0:
            raise ValueError('借款额必须是10的倍数')
        if self._cal_credit_line() < value:
            raise RuntimeError('超过贷款额度')

        self.cash += value
        self.long_liability.add(value, year)

    def _cal_credit_line(self):
        """
        根据权益计算贷款额度
        """
        return LOAN_LIMIT_COEFF * self.equity - \
            sum(self.long_liability) + sum(self.short_liability)

    def update_short_loan(self):
        i, prin = self.short_liability.update()
        self.cash -= i + prin
        self.equity -= i

    def short_loan(self, value):
        """
        在当前季度借短期贷款
        """
        if value % 20 != 0:
            raise ValueError('借款额必须是20的倍数')

        self.cash += value
        self.short_liability.add(value)

    def update_raw_material(self):
        """
        原材料入库/更新原料订单
        """
        price, items = self.logistic.update()
        self.cash -= price
        self.store.put(items)

    def order_raw_material(self, order):
        """
        下原材料订单
        :param order: 原材料订购表
        :type order: dictionary
        """
        self.logistic.order(order)

    def buy_workshop(self, workshop_type: str, slot_id):
        """
        在生产中心的slot_id这个格子上面买一个生产线
        workshop_type是'big','medium','small'
        """
        self.production_center.buy(workshop_type, slot_id)
        cost = int(WORKSHOP[workshop_type+'_price'])
        self.cash -= cost

    def rent_workshop(self, workshop_type: str, slot_id):
        self.production_center.rent(workshop_type, slot_id, rent_season=self.season)
        cost = int(WORKSHOP[workshop_type+'_rent'])
        self.cash -= cost


    def new_line(self, line_type, product_type, workshop_id, slot_id):
        """
        新建生产线
        line_type: 'Flex','Hand','Auto'
        用line_type和product_type构造一个ProductionLine object
        workshop填workshop的slot_id，表示放在那个厂房
        """
        line = eval(line_type + "('" + product_type + "')")

        try:
            self.production_center[workshop_id].add_line(line, slot_id)
        except AttributeError:
            raise RuntimeError('先买或者租了才能建')

        cost = 5    # 新建生产线都是5块，hard code
        self.cash -= cost


    def construct_line(self, workshop_id, line_id):
        """
        把要construct的线放进一个list self.constructed_line，在期末的时候才执行line.construct()
        """
        line = self.check_line_exist(workshop_id, line_id)
        # line.construct()
        self.constructed_line.append(line)

        cost = 5    # 在建生产线都是5块，hard code
        self.cash -= cost


    def sell_line(self, workshop_id, line_id):
        line = self.check_line_exist(workshop_id, line_id)
        # del line
        # getattr(self, workshop+'_workshop').sell_line(line_id)
        self.production_center[workshop_id].sell_line(line_id)

    def switch_product(self, workshop_id, line_id, product_type):
        line = self.check_line_exist(workshop_id, line_id)
        line.switch_product(product_type)

    def update_produce(self, workshop_id, line_id):
        """
        相当于更新生产，把生产线上做好的东西拿出来，放到仓库
        用户点生产按钮的时候，自动执行这个，然后再执行produce
        """
        if self.production_center[workshop_id][line_id].has_product():
            product_type = production_center[workshop_id][line_id].product_type
            self.store.put({product_type: 1})

    def produce(self, workshop, slot_id):
        """
        用workshop和slot_id指定一条生产线开始生产
        判断有没有生产资格，有没有原材料
        """
        line = self.check_line_exist(workshop, slot_id)
        if self.has_certificate(cert=line.product_type) and self.has_raw_material(line):
            cost = line.produce() # 加工费写死了，固定是1，要改就去ProductionLine里面返回加工费
            self.cash -= cost
            components = line.get_material_requirement()
            self.store.take(components)
        else:
            raise RuntimeError(f"还没研发{line.product_type}")

    def has_raw_material(self, line):
        """
        helper method 在生产之前，不影响游戏状态判断一下有没有足够的原材料生产
        """
        components = line.get_material_requirement()
        for r, num in components.items():
            if self.store[r] < int(num):
                raise RuntimeError(f'没有足够的{r}原材料')
        return True



    def retrive_product(self):
        """
        客户端不需要调用这个，在完工入库阶段自动调用
        """
        # for line in self.big_workshop
        pass


    def check_line_exist(self, workshop_id, line_id):
        """
        在做construct_line, sell_line, switch_product, line_produce的时候用的，先
        check生产线存在，再对生产线操作

        返回一个ProductionLine object，对返回的line进行操作
        """
        line = self.production_center[workshop_id][line_id]

        if not line:
            raise ValueError('没有这个生产线')
        return line

    def product_dev(self, product_types: List[str]):
        """
        一个复选款，选了的元素进product_types
        """
        for product_type in product_types:
            if self.certificate[product_type] == 0:
                raise RuntimeError('{} is good to go'.format(product_type))
            self.cash -= int(PRODUCT_DEV_COST[product_type])
            self.certificate[product_type] -= 1
            self.expenditures['产品研发'] += int(PRODUCT_DEV_COST[product_type])

        # 自动调用支付管理费，更新厂房租金
        self.pay_management_cost()
        self.pay_rental_cost()

    def market_dev(self, markets: List[str]):
        """
        input is a list of market ["国内", "本地"] like this
        """
        for market in markets:
            if self.certificate[market] == 0:
                raise RuntimeError("this market is good to go")
            self.cash -= 1
            self.certificate[market] -= 1
            self.expenditures['新市场开拓'] += 1

    def iso_dev(self, isos: List[str]):
        """ input is 'ISO9' or 'ISO14'
        """
        for iso in isos:
            if self.certificate[iso] == 0:
                raise RuntimeError('already have this iso certificate')
            self.cash -= int(ISO_DEV_COST[iso])
            self.certificate[iso] -= 1
            self.expenditures['ISO资格认证'] += int(ISO_DEV_COST[iso])

    def has_certificate(self, cert) -> bool:
        """
        检查有没有研发完某个产品，有没有开市场和ISO那些
        """
        return self.certificate[cert] == 0

    def emergency_buy(self, items_num: dict):
        """
        紧急采购items_num里面的东西
        """
        # 算钱
        for item, num in items_num.items():
            if item[0] == 'r':
                self.cash -= int(MATETIAL_PRICE[item]) * num * int(EMERGENCY_BUY_COEF['raw_material'])
            elif item[0] == 'p':
                self.cash -= PRODUCT_PRICE[item] * num * int(EMERGENCY_BUY_COEF['product'])
        # 放进仓库
        self.store.put(items_num)

    def get_order(self, order_id):
        """
        拿订单
        """
        # TODO: 把判断能不能拿交给闰土搞条件按钮
        # ISO9, ISO14 = id_order[order_id][5], id_order[order_id][6]
        # if ISO9 and not self.certificate['ISO9']:
        #     raise
        self.obtain_order.add(order_id=order_id)


    def delivery(self, order_id):
        """
        提交订单编号为order_id的订单
        """
        product_type, num, index = self.obtain_order.pre_delivery(order_id)
        # 判断有没有足够库存
        if not self.store[product_type] >= num:
            raise RuntimeError("产品不足，无法提交订单")
        # 足够，再进行下一步，调用self.obtain_order.delivery()
        # 看这张单能拿到多少账期的多少钱
        money, account_period = self.obtain_order.delivery(index, order_id)
        # 0账期的直接加现金，其他加应收款
        if account_period == 0:
            self.cash += money
        else:
            self.receivables.add(num=money, period=account_period)

    def discount_receiable(self, period_values: dict):
        """
        period_values是key为1234，value是贴现金额的dict
        """
        i, prin = self.receivables.discount(period_values)
        # 记录财务费用
        self.income_statement['财务费用'] += i
        # 现金增加
        self.cash += prin

    def depreciate(self):
        """
        对所有厂房里面的所有生产线折旧，统计折旧额到利润表

        年末必须先折旧，然后再end_season()，
        """
        count = 0
        for workshop in self.production_center:
            if not workshop:
                continue
            for line in workshop:
                count_ = line.depreciate()
                count += count_
        self.income_statement['累计折旧'] = count

    '''
    自动调用的方法
    '''
    def pay_management_cost(self):
        """
        支付管理费

        在产品研发投资之后自动调用
        """
        self.expenditures['管理费用'] += 1
        self.cash -= 1

    def pay_rental_cost(self):
        """
        支付厂房租金

        在产品研发投资之后自动调用
        """
        total = 0
        for workshop in self.production_center:
            if workshop is not None:
                total += workshop.get_rental_cost(self.season)

        self.expenditures['厂房租金'] = total
        self.cash -= total




class CompanyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
