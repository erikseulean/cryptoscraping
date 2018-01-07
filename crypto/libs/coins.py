from crypto.data.loader import cleaned_dataset
from datetime import datetime as Date
import pandas as pd
import json

class Coins:

    #TODO to be refactored to use a proper datastore
    def __load_dataset__(self):
        return cleaned_dataset()

    def __load_exchanges__(self):
        exchanges = json.load(open('crypto/data/dict.json'))
        exchange_symbols = {}
        for exch, coins in exchanges.items():
            symbols = []
            for coin in coins:
                symbols.append(self.dataset[self.dataset["Coin"] == coin]["Symbol"].values[0])
            exchange_symbols[exch] = symbols
        return exchange_symbols

    def __init__(self, dataset = None, exchanges = None):
        self.dataset = dataset if dataset else self.__load_dataset__()
        self.exchanges_dataset = exchanges if exchanges else self.__load_exchanges__()

        # rename coins to symbols

    def coin_data(self, coin, field):
        name = field["field"]
        if name == "EXCHANGES":
            return self._get_exchanges_coin(coin)

        if name == "AGE":
            return self._get_age_coin(coin)

        if name == "ICO":
            return self._get_ico_date(coin)

    def price(self, greather_or_equal_than, smaller_or_equal_than, as_of_date = None):
        """Filter coins based on price"""
        working_data = pd.DataFrame(self.dataset)
        # First, filter by date:
        if as_of_date is None:
            as_of_date = Date.today().date()
        working_data = working_data[working_data["Date"] == as_of_date]

        # Second, filter by price:
        working_data = working_data[
                        (working_data["Close"] >= greather_or_equal_than) &
                        (working_data["Close"] <= smaller_or_equal_than)]

        return working_data

    def exchanges(self, exchange_names):
        """Filter coins within these exchanges"""
        all_currencies = set()
        for name in exchange_names:
            all_currencies = all_currencies | set(self.exchanges_dataset[name])
        return all_currencies

    def new_coins(self, start_date, end_date):
        coins_as_of_start_date = \
            set(self.dataset[self.dataset["Date"] == start_date]["Symbol"])

        coins_as_of_end_date = \
            set(self.dataset[self.dataset["Date"] == end_date]["Symbol"])

        return [item for item in coins_as_of_end_date \
                      if item not in coins_as_of_start_date]

    def _get_ico_date(self, coin):
        dt = min(self.dataset[self.dataset["Symbol"] == coin]["Date"].values)
        dt = pd.to_datetime(dt).to_datetime()
        return dt

    def _get_age_coin(self, coin):
        ico_date = self._get_ico_date(coin)
        today = Date.today()
        diff_in_seconds = (today - ico_date).total_seconds()
        return (round(diff_in_seconds/(60*60*24*7*52),2))

    def _get_exchanges_coin(self, coin):
        coin_exchanges = []
        for exchange, coins in self.exchanges_dataset.items():
            if coin in coins:
                coin_exchanges.append(exchange)

        return coin_exchanges
