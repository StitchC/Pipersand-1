import configparser
config = configparser.ConfigParser()
try:
    config.read_file(open('Sandbox/core/setting.ini'))
except:
    config.read('setting.ini')



from collections import deque


class Logistic(object):
    # 空仓库，初始化的时候用的
    zero_material = {}
    for key in config['raw material']:
        zero_material[key] = 0

    # 最慢的原材料运输周期
    shipping_time = config['raw material shipping time']
    longest_period = max(int(x) for x in shipping_time.values())

    def __init__(self):
        # material_in_transit是在途原材料
        # : type : Deque([dict]) deque of list of dict
        self.material_in_transit = deque()
        for _ in range(Logistic.longest_period):
            self.material_in_transit.append(Logistic.zero_material.copy())

    def __getitem__(self, index):
        return self.material_in_transit[index - 1]

    def update(self):
        price = 0   # 需要支付的货款
        for material, num in self.material_in_transit[0].items():
            price += num * int(config['raw material price'][material])  # 数量 * 单价

        items = self.material_in_transit.popleft()
        self.material_in_transit.append(Logistic.zero_material.copy())

        return price, items

    def order(self, order):
        """
        下原材料订单
        :param order: 原材料订购表
        :type order: dictionary
        """
        for material, num in order.items():
            period = int(Logistic.shipping_time[material])  # 该原材料的运输周期
            self.material_in_transit[period - 1][material] += num
