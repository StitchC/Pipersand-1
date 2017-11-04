# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 22:05:08 2017

@author: schmidt
"""
'''
attribute:
    product_type: 产品类型
    produce_process: 还有几个季度生产完
    switch_process: 还有几个季度转产完
    _status: 建成需要季度
    _net_value: 净值

method:
    construct(): 在建生产线
    depreciate(): 折旧
    produce(): 生产产品
    has_product(): 是否有产品


'''

import configparser
config = configparser.ConfigParser()
config.read('C:/Users/67089/Documents/GitHub/Pipersand/Sandbox/core/setting.ini')
PRODUCT_COMPONENT = {}  # dict of dict
for product in ['p1', 'p2', 'p3', 'p4']:
    components = product + ' components'
    PRODUCT_COMPONENT[product] = config[components]


class ProductionLine(object):
    """

    """

    def __init__(self, product_type):
        self.product_type = product_type
        self.switch_process = 0
        self.produce_process = 0
        self.new = True

    def __str__(self):
        return '{}, net_value is {}, status is {}'.format(
            self.__class__.__name__,
            self._net_value,
            self._status)

    def reprJSON(self):
        return dict(product_type=self.product_type,
                    switch_process=self.switch_process,
                    produce_process=self.produce_process,
                    new=self.new)

    def depreciate(self):
        """
        折旧
        返回折旧值
        """
        # 还未建成不用折旧
        if self._status != 0:
            return 0

        # 新的生产线不用折旧
        if self.new is True:
            self.new = False
            return 0

        # 已经折旧到残值不用折旧
        if self._net_value <= self._salvage_value:
            return 0

        self._net_value -= self._depreciate_value
        return self._depreciate_value

    def construct(self):
        if self._status > 0:
            self._net_value += 5
            self._status -= 1
        else:
            raise RuntimeError('this line is already constructed')


    def has_product(self):
        """
        end_season()的时候调用

        在生产产品之前判断线上有没有产品，然后把生产计时重置
        返回出产的产品类型
        """
        if self.produce_process == 0:
            self.produce_process = self._produce_period  # reset produce_process
            return True
        else:
            return False

    def get_material_requirement(self):
        return PRODUCT_COMPONENT[self.product_type]

    def produce(self):
        """
        生产产品
        返回支付了多少加工费
        """
        if self._status != 0 or self.switch_process != 0:
            raise RuntimeError('this line is not avaliable now')

        # 判断是不是刚放进去生产的，是就要给加工费
        if self.produce_process == self._produce_period:
            cost = 1    # 加工费是1，写死
        else:
            cost = 0

        self.produce_process -= 1

        return cost

    def switch_product(self, product_type):
        """override in subclasses"""
        pass

    @property
    def product_type(self):
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        self._product_type = value


class Hand(ProductionLine):
    def __init__(self, product_type):
        self._depreciate_value = 1
        self._salvage_value = 1
        self._net_value = 5

        self._produce_period = 3

        self._status = 0

        super().__init__(product_type)

    def switch_product(self, product_type):
        if self.product_type == product_type:
            pass
        else:
            self.product_type = product_type


class Auto(ProductionLine):
    def __init__(self, product_type):
        self._depreciate_value = 3
        self._salvage_value = 3
        self._net_value = 5

        self._produce_period = 1

        self._status = 2

        super().__init__(product_type)

    def switch_product(self, product_type=None):
        if self.switch_process != 0 and product_type is not None:
            raise RuntimeError("this line is swithching")
        if self.product_type == product_type:
            raise RuntimeError("this line's product_type is {}".format(self.product_type))

        if product_type is None and self.switch_process > 0:
            self.switch_process -= 1
            return
        self.product_type = product_type
        self.switch_process = 2


class Flex(ProductionLine):
    def __init__(self, product_type):
        self._depreciate_value = 4
        self._salvage_value = 4
        self._net_value = 5

        self._produce_period = 1

        self._status = 3

        super().__init__(product_type)

    def switch_product(self, product_type=None):
        if self.product_type == product_type:
            raise RuntimeError("this line's product_type is {}".format(self.product_type))
        self.product_type = product_type
