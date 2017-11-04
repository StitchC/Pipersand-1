import configparser
config = configparser.ConfigParser()
config.read('C:/Users/67089/Documents/GitHub/Pipersand/Sandbox/core/setting.ini')
PRODUCTION_CENTER_CAPACITY = config['production center capacity']


from ..core.Workshop import Workshop



class ProductionCenter(object):
    """
    直接PRODUCTION_CENTER_CAPACITY['num_workshop']个厂房写死
    用来存厂房的，ProductionCenter里面是厂房，厂房里面是生产线
    """
    def __init__(self):
        self.workshops = [None for _ in range(int(PRODUCTION_CENTER_CAPACITY['num_workshop']))]

    def __getitem__(self, index):
        return self.workshops.__getitem__(index - 1)

    def reprJSON(self):
        return dict(workshops=self.workshops)

    def __len__(self):
        """
        有多少个厂房(self.workshops中非None个数)
        """
        # return self.workshops.__len__()
        return sum(1 for workshop in self.workshops if workshop)

    def buy(self, workshop_type: str, slot_id: int):
        """
        改厂房的状态或者
        调用..core.Workshop.Workshop()创建一个厂房，然后加到slot里面
        """
        ### 之前状态是租的，现在买进来，直接改状态
        if self.workshops[slot_id - 1] and self.workshops[slot_id - 1].status == 'rent':
            self.workshops[slot_id - 1].status = 'buy'
            return

        ### 之前没有租的，创建一个新的厂房
        capacity = int(PRODUCTION_CENTER_CAPACITY[workshop_type])
        workshop = Workshop(capacity=capacity, workshop_type=workshop_type, status='buy')
        # TODO: 闰土判断这个slot是不是空的，别把原来有的厂房覆盖掉了
        # TODO: 状态已经是买的时候，不能在网页的slot_id这个位置点买生产线
        self.workshops[slot_id - 1] = workshop

    def rent(self, workshop_type: str, slot_id: int, rent_season):
        """
        调用..core.Workshop.Workshop()创建一个厂房，然后加到slot里面
        记录租厂房的时候是第几季度
        """
        capacity = int(PRODUCTION_CENTER_CAPACITY[workshop_type])
        workshop = Workshop(capacity=capacity, workshop_type=workshop_type, status='rent')
        # 记录第几季度租的
        workshop.rent_season = rent_season
        self.workshops[slot_id - 1] = workshop

    def sell(self, slot_id):
        """
        卖掉slot_id号厂房,返回得到多少账期的多少钱
        """
        # TODO: 闰土判断状态不是'buy'的厂房不能卖,卖的按钮是灰色
        pass
