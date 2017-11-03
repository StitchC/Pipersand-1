from ..core.custom_orders import id_order




class Order(object):
    def __init__(self, product_type, num, price, delivery_period, account_period,
                    iso9: bool, iso14: bool, market: str):
        self.product_type = product_type
        self.num = num
        self.delivery_period = delivery_period
        self.account_period = account_period

    def reprJSON(self):
        return dict(product_type=self.product_type,
                    num=self.num,
                    delivery_period=self.delivery_period,
                    account_period=self.account_period)


class ObtainOrder(object):
    """
    属于某个公司的订单，类似company.workshop
    """
    def __init__(self):
        self.orders = []
        # 3种状态，producing, delivered, failed

    def reprJSON(self):
        return dict(orders=self.orders)

    def add(self, order_id):
        """
        接订单
        """
        self.orders.append([order_id, 'producing'])   # 订单的编号和订单的交货状态

    def pre_delivery(self, order_id):
        """
        交订单之前在company.obtain_order那边调用看看能不能交货，如果可以就在company那边
        继续调用delivery(order_id)
        """
        index = None
        # 找到那张订单在orders里面的index
        for i in range(len(self.orders)):
            if self.orders[i][0] == order_id and self.orders[i][1] == 'producing':
                index = i
                break
        else:
            raise RuntimeError(f"不存在这个订单，订单编号: {order_id}")

        # 返回需要交货的产品类型，数量，还有index，留给delivery用的
        # index是在自己拿到的订单里面是第几张
        return id_order[order_id].product_type, id_order[order_id].num, index

    def delivery(self, index, order_id):
        """
        index参数是pre_delivery返回的
        """
        # 把订单状态设为已交货
        self.orders[index][1] = 'delivered'
        # 返回得到多少钱，多少账期
        return id_order[order_id].price, id_order[order_id].account_period
