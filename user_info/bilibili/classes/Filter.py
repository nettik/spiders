from pybloom_live import ScalableBloomFilter


class Filter():
    def __init__(self, capacity=500000):
        self.filter = ScalableBloomFilter(initial_capacity=capacity)

    def is_id_in_filter(self, userid):
        return userid in self.filter

    def add_in_filter(self, userid):
        self.filter.add(userid)
