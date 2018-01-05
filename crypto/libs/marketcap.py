from datetime import datetime
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