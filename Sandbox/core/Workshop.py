# from production_line import *


class Workshop(object):
    def __init__(self, capacity, status=None):
        self.status = status  # buy, rent or none
        self.lines = [None for _ in range(capacity)]
        self.capacity = capacity

    def __iter__(self):
        return self.lines.__iter__()

    def __getitem__(self, index):
        return self.lines[index - 1]

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
