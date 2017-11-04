# from production_line import *
import configparser
config = configparser.ConfigParser()
config.read('C:/Users/67089/Documents/GitHub/Pipersand/Sandbox/core/setting.ini')
WORKSHOP = config['workshop']


class Workshop(object):
    def __init__(self, capacity, workshop_type, status=None):
        self.workshop_type = workshop_type
        self.rent_season = None
        self.status = status  # 'buy', 'rent' or none
        self.lines = [None for _ in range(capacity)]
        self.capacity = capacity

    def __iter__(self):
        return self.lines.__iter__()

    def __getitem__(self, index):
        return self.lines[index - 1]

    def reprJSON(self):
        return dict(status=self.status,
                    lines=self.lines,
                    capacity=self.capacity)

    def get_rental_cost(self, season):
        """
        返回这个厂房在season季度需要支付的租金
        """
        # 不是租的不用交租金
        if self.status != 'rent':
            return 0

        # 不是这个季度租的不用交
        if self.rent_season != season:
            return 0

        return int(WORKSHOP[self.workshop_type + '_rent'])



    def add_line(self, line, slot_id):
        """
        :param line: 添加到厂房中的生产线
        :type line: ProductionLine
        """
        if self.status is None:
            raise RuntimeError("先租或者买了厂房才能建生产线")
        # TODO: 前端判断，如果已经有生产线在这个格，不能点这个按钮
        # if len(self.lines) == self.capacity:
        #     raise RuntimeError("没有空余的位置放置生产线")

        self.lines[slot_id - 1] = line

    def sell_line(self, slot_id):
        """
        :param slot_id: 要出售的生产线的ID
        :type slot_id: integer
        """
        self.lines[slot_id - 1] = None
