from datetime import datetime as Date

class MarketCap(Object):

    def __init__(self, dataset):
        self.dataset = dataset;

    def current(self, coin, measurement_coin, exchange=''):
        pass

    def historical(self, coin, measurement, coin, exchange=''):
        pass

    def top(number_of_coins, as_of_date=None):
        pass

    def range(lower_bound, upper_bound, as_of_date = None):
        pass

    def smaller(upper_bound, as_of_date = None):
        pass

    def bigger(lower_bound, as_of_date = None):
        pass

    def between(lower_bound, upper_bound, as_of_date = None):
        pass
