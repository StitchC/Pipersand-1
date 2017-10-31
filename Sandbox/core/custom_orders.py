"""
手动录入订单
Order(product_type, num, price, account_period, delivery_period,
            iso9: bool, iso14: bool, market: str)
"""


# from Sandbox.core.Order import Order
# TODO: why can not import????
class Order(object):
    def __init__(self, product_type, num, price, delivery_period, account_period,
                    iso9: bool, iso14: bool, market: str):
        self.product_type = product_type
        self.num = num
        self.price = price
        self.delivery_period = delivery_period
        self.account_period = account_period
        self.iso9 = iso9
        self.iso14 = iso14


id_order = {1: Order(product_type='p1', num=5, price=15, delivery_period=2,
                        account_period=0, iso9=0, iso14=1, market='本地'),
            2: Order(product_type='p1', num=6, price=30, delivery_period=3,
                        account_period=4, iso9=1, iso14=1, market='区域'),
            'test': Order(product_type='p2', num=3, price=15, delivery_period=3,
                        account_period=0, iso9=1, iso14=0, market='本地'),
            'test1': Order('p2', 3, 15, 3, 3, 1, 0, market='国内')}


"""
随机生成订单
"""
# 设置规则
# 本地订单数
bendi_num_order = 10
# P1平均单价
bendi_p1_price = 0
# P2平均单价
bendi_p2_price = 0
# P3平均单价
bendi_p3_price = 0
# P4平均单价
bendi_p4_price = 0
# 价格浮动方差
bendi_price_std = 3


# 区域订单数
quyu_num_order = 10
# P1平均单价
quyu_p1_price = 0
# P2平均单价
quyu_p2_price = 0
# P3平均单价
quyu_p3_price = 0
# P4平均单价
quyu_p4_price = 0
# 价格浮动方差
quyu_price_std = 3


# 国内订单数
guonei_num_order = 10
# P1平均单价
guonei_p1_price = 0
# P2平均单价
guonei_p2_price = 0
# P3平均单价
guonei_p3_price = 0
# P4平均单价
guonei_p4_price = 0
# 价格浮动方差
guonei_price_std = 3
# 亚洲订单数
# 国际订单数




# 测试用的
