import configparser
config = configparser.ConfigParser()
config.read('Sandbox/core/setting.ini')
DISCOUNT_RATE12 = float(config['discount rate']['period12'])
DISCOUNT_RATE34 = float(config['discount rate']['period34'])


import numpy as np
from collections import deque


class Receivables(object):
    """
    一个列表，self.recei[0]是1账期应收款，..., self.recei[3]是4账期应收款
    """

    def __init__(self):
        self.recei = deque([0, 0, 0, 0])

    def update(self):
        """返回零账期的应收款金额，其他的往前推一格"""
        cash = self.recei[0]
        self.recei.popleft()
        self.recei.append(0)
        return cash

    def __str__(self):
        return "1账期{}，2账期{}，3账期{}，4账期{}".format(*self.recei)

    def __getitem__(self, index):
        return self.recei[index - 1]

    def discount(self, period_values: dict):
        """
        贴现应收款，返回贴息和得到的现金
        period_values是key为1234，value是贴现金额的dict
        """
        # 先check有没有这么多应收款, 扣钱, 统计12期34期贴现总数
        sum_12, sum_34 = 0, 0
        for period, value in period_values.items():
            if self.recei[period - 1] < value:
                raise RuntimeError('no that amount of receivable')
            self.recei[period - 1] -= value

            if period in [1, 2]:
                sum_12 += value
            elif period in [3, 4]:
                sum_34 += value

        i = np.ceil(DISCOUNT_RATE12 * sum_12) + np.ceil(DISCOUNT_RATE34 * sum_34)
        return i, sum_12+sum_34-i

    def add(self, num, period):
        self.recei[period - 1] += num


class Long_lia(object):
    def __init__(self):
        self.lia = deque([0, 0, 0, 0, 0, 0])
        self.interest_rate = 0.1

    def __iter__(self):
        return iter(self.lia)

    def __str__(self):
        return "一年到期{}，两年到期{}，三年到期{}，四年到期{}，五年到期{}，六年到期{}".format(*self.lia)

    def __getitem__(self, index):
        return self.lia.__getitem__(index-1)

    def update(self):
        """
        :returns i: 需要还的利息
        :returns prin: 需要还的本金
        """
        i = sum(self.lia) * self.interest_rate
        prin = self.lia[0]
        self.lia.popleft()
        self.lia.append(0)
        return i, prin

    def add(self, value, year):
        self.lia[year - 1] += value


class Short_lia(object):
    def __iter__(self):
        return iter(self.lia)

    def __init__(self):
        self.lia = deque([0, 0, 0, 0])
        self.interest_rate = 0.05

    def __getitem__(self, index):
        return self.lia.__getitem__(index-1)

    def add(self, value):
        self.lia[3] += value

    def update(self):
        prin = self.lia[0]
        i = prin * self.interest_rate
        self.lia.popleft()
        self.lia.append(0)
        return i, prin

    def __str__(self):
        return "还有一季到期{}，还有二季到期{}，还有三季到期{}，还有四季到期{}".format(*self.lia)
