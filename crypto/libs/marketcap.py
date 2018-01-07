from datetime import datetime
from heapq import heappush, heappop, heapreplace, nlargest
from coinmarketcap.recent_data import get_current_values
from crypto.data.loader import cleaned_dataset
from crypto.libs import dateutils

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

        coin_market_cap = data[(data['Symbol'] == coin)]['Market-Cap'].values[0]
        if measurement == 'usd':
            return coin_market_cap

        measurement_price = data[(data['Symbol'] == measurement)]['Close'].values[0]
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

    def _transform_(self, dataset):
            result = []
            for index, row in dataset.iterrows():
                result.append((row['Symbol'], row['Market-Cap']))
            return result

    def top(self, number_of_coins, as_of_date=None):
        if as_of_date is None:
            return self._top_today_(number_of_coins)

        data = self.dataset[(self.dataset['Date'] == as_of_date)]
        data = data.sort_values('Market-Cap', ascending=False)
        return self._transform_(data[0:number_of_coins])

    def _between_today_(self, lower_bound = None, upper_bound = None):
        current = get_current_values()
        return [
            (float(data['market_cap_usd']), coin) for coin, data in current.items()
            if data['market_cap_usd'] and (
                (float(data['market_cap_usd']) >= lower_bound if lower_bound else True) and
                (float(data['market_cap_usd']) <= upper_bound if upper_bound else True)
            )
        ]

    def _between_historical_(self, as_of_date, lower_bound = None, upper_bound = None):
        data = self.dataset[self.dataset['Date'] == as_of_date]
        if lower_bound:
            data = data[data['Market-Cap'] >= lower_bound]
        if upper_bound:
            data = data[data['Market-Cap'] <= upper_bound]
        return self._transform_(data)

    def range(self, lower_bound, upper_bound, as_of_date = None):
        if as_of_date is None:
            as_of_date = datetime.today().date()

        data = self.dataset[(self.dataset['Date'] == as_of_date)]
        data = data.sort_values('Market-Cap', ascending=False)
        return self._transform_(data[lower_bound:upper_bound])


    def smaller(self, upper_bound, as_of_date = None):
        if as_of_date is None:
            return self._between_today_(upper_bound = upper_bound)
        return self._between_historical_(as_of_date, upper_bound = upper_bound)

    def bigger(self, lower_bound, as_of_date = None):
        if as_of_date is None:
            return self._between_today_(lower_bound = lower_bound)
        return self._between_historical_(as_of_date, lower_bound = lower_bound)

    def between(self, lower_bound, upper_bound, as_of_date = None):
        greater_than = set(self.smaller(upper_bound, as_of_date))
        lower_than = set(self.bigger(lower_bound, as_of_date))
        return set(greater_than).intersection(lower_than)

    def total(self, start_date = None, end_date = None):

        if start_date is None and end_date is None:
            start_date = datetime.today().date()

        if end_date is not None:
            result = {}
            date_range = dateutils.dateRange(start_date, end_date, 1, "d")
            for date in date_range:
                todays_data = self.dataset[self.dataset["Date"] == date]
                result[date] = sum(todays_data["Market-Cap"].dropna())
            return result
        else:
            todays_data = self.dataset[self.dataset["Date"] == start_date]
            return sum(todays_data["Market-Cap"].dropna())

    def share(self, coin, start_date = None, end_date = None):
        result = None

        if start_date is None and end_date is None:
            start_date = datetime.today().date()

        if end_date is not None:
            result = {}
            date_range = dateutils.dateRange(start_date, end_date, 1, "d")
            for date in date_range:
                total_at_date = self.total(date)
                coin_marketcap = self.historical(coin, "usd", date)
                coin_share = coin_marketcap / total_at_date * 100
                result[date] = coin_share
        else:
            total_at_date = self.total(start_date)
            coin_marketcap = self.historical(coin, "usd", start_date)
            coin_share = coin_marketcap / total_at_date * 100
            result = coin_share
        return result

    def rank(self, coin, start_date = None, end_date = None):
        result = None

        if start_date is None and end_date is None:
            start_date = datetime.today().date()

        if end_date is not None:
            result = {}
            date_range = dateutils.dateRange(start_date, end_date, 1, "d")
            for date in date_range:
                todays_data = self.dataset[(self.dataset["Date"] == start_date)]
                todays_data = todays_data.sort_values(by="Market-Cap", ascending=False)
                todays_data.index = range(1, len(todays_data)+1)
                rank = todays_data[todays_data["Symbol"] == coin].index
                result[date] = rank.values[0]

        else:
            todays_data = self.dataset[(self.dataset["Date"] == start_date)]
            todays_data = todays_data.sort_values(by="Market-Cap", ascending=False)
            todays_data.index = range(1, len(todays_data)+1)
            rank = todays_data[todays_data["Symbol"] == coin].index
            result = rank.values[0]
        return result
