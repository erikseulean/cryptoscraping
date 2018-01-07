import requests
import datetime
import pandas as pd
from datetime import datetime as Date

class Price:
    def __init__(self):
        pass

    def _historical_add_url_frequency(self, bar_type, bar_size):
        url_request_period = "histoday"

        if bar_type == "h":
            url_request_period = "histohour"
        elif bar_type == "m":
            url_request_period = "histominute"
        elif bar_type == "d":
            url_request_period = "histoday"
        elif bar_type == "w":
            bar_size = bar_size * 7
            url_request_period = "histoday"
        elif bar_type == "M":
            bar_size = bar_size * 30.5
            url_request_period = "histoday"
        else:
            url_request_period = "histoday"

        return url_request_period, bar_size

    def _historical_invert_dates(self, start_datetime, end_datetime):
        if start_datetime is not None and end_datetime is not None:
            swap_aux = end_datetime
            end_datetime = start_datetime
            start_datetime = swap_aux

        return start_datetime, end_datetime

    def _historical_only_one_date(self, start_datetime, end_datetime, num_points):
        if end_datetime is not None and \
           start_datetime is None and \
           num_points is None:
           num_points = 1
        return num_points

    def _historical_set_num_points(self, url, start_datetime, end_datetime, num_points):
        if start_datetime is None:
            if num_points is None:
                url += '&allData=true'
            else:
                url += '&limit={}'.format(num_points)
        else:
            num_days = (end_datetime - start_datetime).total_seconds()
            num_days = num_days / (60*60*24)
            if num_points is None:
                num_points = num_days
            url += '&limit={}'.format(num_points)

        return url

    def historical( self, base_coin, traded_coin, end_datetime = None, start_datetime = None,
                    bar_type = "d", bar_size = 1, num_points = None, fields = ["close"],
                    sort = None, exchange = ''):
        """
        Historical data returned in bar format.
        example:
        bar_type = "d" and bar_size="1"  -> returns every day price close and interval volume
        bar_type = "m" and bar_size="30" -> returns data every 30 minutes

        if you want every 1 minute -> bar_size = 1 bar_type = "m"
        if you want every 7 days -> bar_size = 7 and bar_type = "d"

        """

        # Setting up url for frequency
        url_request_period, bar_type = self._historical_add_url_frequency(
                                            bar_type, bar_size)

        url = 'https://min-api.cryptocompare.com/data/{}?fsym={}&tsym={}&aggregate={}'\
                .format(url_request_period, base_coin.upper(), traded_coin.upper(), bar_size)

        # Set exchange
        if exchange:
            url += '&e={}'.format(exchange)

        # Swapping dates to facilitate optional args for the user
        start_datetime, end_datetime = self._historical_invert_dates(
                                            start_datetime, end_datetime)

        # Set end date time. We take it back from then.
        end_date_timestamp = (end_datetime - Date(1970, 1, 1)).total_seconds()
        url += "&toTs={}".format(int(end_date_timestamp))

        # Set how much data to get back
        num_points = self._historical_only_one_date(
                          start_datetime, end_datetime, num_points)

        url = self._historical_set_num_points(
                   url, start_datetime, end_datetime, num_points)


        page = requests.get(url)
        data = page.json()['Data']
        df = pd.DataFrame(data)
        #print (start_datetime, end_datetime, url)
        try:
            df.index = [Date.fromtimestamp(d) for d in df.time]
            df = df[fields]
            if num_points == 1:
                return df.head(1)
        except:
            print ("Error on calling {}, got error {}".format(url, page.json()))
        return df

    def current(self, base_coin, traded_coin = "USD", exchange='Bitstamp'):
        url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
                .format(base_coin.upper(), ','.join([traded_coin]).upper())
        if exchange:
            url += '&e={}'.format(exchange)

        page = requests.get(url)
        data = page.json()
        if "Response" in data.keys() and "Error" == data["Response"]:
            print ("Error on calling {}, got error {}".format(url, data["Message"]))
            data = None

        data = data[traded_coin]
        return data

    def change(self, base_coin, traded_coin,
               start_date, end_date, exch='Bitstamp'):
        final_price = self.historical(base_coin, traded_coin, end_date, exchange = exch)
        final_price = final_price["close"].values[0]

        initial_price = self.historical(base_coin, traded_coin, start_date, exchange = exch)
        initial_price = initial_price["close"].values[0]

        return round((final_price / initial_price - 1) * 100, 2)
