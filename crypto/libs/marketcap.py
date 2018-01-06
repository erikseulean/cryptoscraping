from datetime import datetime
from heapq import heappush, heappop, heapreplace, nlargest
from coinmarketcap.recent_data import get_current_values
from crypto.data.loader import cleaned_dataset

class MarketCap:

    #TODO to be refactored to use a proper datastore
    def __load__(self):
        return cleaned_dataset()

    def __init__(self, dataset = None):
        self.dataset = dataset if dataset else self.__load__()

    def current(self, coin, measurement_coin):
        current = get_current_values()
        if measurement_coin == 'usd':
            return current[coin]['market_cap_usd']

        measurerment_coin_price = float(current[measurement_coin]['price_usd'])
        return float(current[coin]['market_cap_usd']) / measurerment_coin_price

    def historical(self, coin, measurement, date):
        data = self.dataset[(self.dataset['Date'] == date)]

        coin_market_cap = data[(data['Coin'] == coin)]['Market-Cap'].values[0]
        if measurement == 'usd':
            return coin_market_cap

        measurement_price = data[(data['Coin'] == measurement)]['Close'].values[0]
        return coin_market_cap / measurement_price

    def _top_today_(self, number_of_coins):
        current = get_current_values()
        top = []
        for coin, data in current.items():
            if not data['market_cap_usd']:
                continue

            marketcap = float(data['market_cap_usd'])

            if len(top) < number_of_coins:
                heappush(top, (marketcap, coin))
            else:
                if top[0][0] < marketcap:
                    heapreplace(top, (marketcap, coin))

        return nlargest(number_of_coins, top)

    def top(self, number_of_coins, as_of_date=None):
        if as_of_date is None:
            return self._top_today_(number_of_coins)

        def transform(dataset):
            result = []
            for index, row in dataset.iterrows():
                result.append((row['Market-Cap'], row['Coin']))
            return result

        data = self.dataset[(self.dataset['Date'] == as_of_date)]
        data = data.sort_values('Market-Cap', ascending=False)
        return transform(data[0:number_of_coins])

    def _range_today_(self, lower_bound, upper_bound):
        current = get_current_values()
        return [
            (float(data['market_cap_usd']), coin) for coin, data in current.items()
            if data['market_cap_usd'] and (
                float(data['market_cap_usd']) >= lower_bound and float(data['market_cap_usd']) <= upper_bound
            )
        ]


    def range(self, lower_bound, upper_bound, as_of_date = None):
        if as_of_date is None:
            return self._range_today_(lower_bound, upper_bound)

    def smaller(self, upper_bound, as_of_date = None):
        pass

    def bigger(self, lower_bound, as_of_date = None):
        pass

    def between(self, lower_bound, upper_bound, as_of_date = None):
        pass
