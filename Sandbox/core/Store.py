class Store(object):
    def __init__(self):
        self.store = {'r1': 0,
                      'r2': 0,
                      'r3': 0,
                      'r4': 0,
                      'p1': 0,
                      'p2': 0,
                      'p3': 0,
                      'p4': 0,
                      }

    def __getitem__(self, key):
        return self.store.__getitem__(key)

    def put(self, items: dict):
        for item, num in items.items():
            self.store[item] += num

    def take(self, items: dict):
        for item, num in items.items():
            self.store[item] -= int(num)

    def get_inventory(self):
        return self.store
