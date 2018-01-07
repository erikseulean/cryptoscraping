import requests
import datetime
import pandas as pd
from crypto.data.loader import cleaned_dataset
from datetime import datetime as Date

class Price:

    #TODO to be refactored to use a proper datastore
    def __load__(self):
        return cleaned_dataset()

    def __init__(self, dataset = None):
        self.dataset = dataset if dataset else self.__load__()

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
            return end_datetime, start_datetime
        else:
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
                    sort = None, exchange = None):
        """
        Historical data returned in bar format.
        example:
        bar_type = "d" and bar_size="1"  -> returns every day price close and interval volume
        bar_type = "m" and bar_size="30" -> returns data every 30 minutes

        if you want every 1 minute -> bar_size = 1 bar_type = "m"
        if you want every 7 days -> bar_size = 7 and bar_type = "d"

        """

        # Setting up url for frequency
        url_request_period, bar_size = self._historical_add_url_frequency(
                                            bar_type, bar_size)

        url = 'https://min-api.cryptocompare.com/data/{}?fsym={}&tsym={}&aggregate={}'\
                .format(url_request_period, base_coin.upper(), traded_coin.upper(), bar_size)

        # Swapping dates to facilitate optional args for the user
        # Inverting only if they are both not None
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

        # Set exchange
        if exchange is not None:
            url += '&e={}'.format(exchange)


        ### If we want a specific exchange, we get from cryptocompare
        ### Otherwise we get from the scraped data
        if exchange is None and \
           (bar_type == 'd' or bar_type == 'w' or bar_type=='M'):
           return self._get_scraped_historical_data(base_coin,
                                                    traded_coin,
                                                    start_datetime,
                                                    end_datetime,
                                                    num_points)
        if exchange is not None and \
            (bar_type == 'd' or bar_type == 'w' or bar_type=='M') and \
            num_points == 1:
            return self._get_historical_date_point_of_exchange(base_coin,
                                                               traded_coin,
                                                               end_datetime,
                                                               exchange)
        page = requests.get(url)
        data = page.json()['Data']
        df = pd.DataFrame(data)
        #print (start_datetime, end_datetime, url)
        try:
            if bar_type == 'd' or bar_type == 'w' or bar_type=='M':
                df.index = [Date.fromtimestamp(d).date() for d in df.time]
            else:
                df.index = [Date.fromtimestamp(d) for d in df.time]
            df = df[fields]
            if num_points == 1:
                return df.head(1)
        except:
            print ("Error on calling {}, got error {}".format(url, page.json()))
        return df

    def _get_scraped_historical_data(self,
                                     base_coin,
                                     traded_coin,
                                     start_datetime,
                                     end_datetime,
                                     num_points):
        if start_datetime is None and end_datetime is not None:
           start_datetime = end_datetime

        base_working_data = self.dataset[self.dataset["Symbol"] == base_coin]
        base_working_data = base_working_data[(base_working_data["Date"] >= start_datetime) &
                                    (base_working_data["Date"] <= end_datetime)]

        traded_working_data = self.dataset[self.dataset["Symbol"] == traded_coin]
        traded_working_data = traded_working_data[(traded_working_data["Date"] >= start_datetime) &
                                    (traded_working_data["Date"] <= end_datetime)]

        if (start_datetime == end_datetime):
            base_working_data = base_working_data[["Close"]]
            if traded_coin == "USD":
                return base_working_data["Close"].values[0]
            else:
                traded_to_usd = traded_working_data["Close"].values[0]
                return base_working_data["Close"].values[0] / traded_to_usd
        else:
            if num_points is not None:
                base_working_data = base_working_data.head(num_points)

            base_working_data.index = base_working_data["Date"].values
            base_working_data = base_working_data[["Close"]]
            base_working_data.columns = [["close"]]
            if traded_coin == "USD":
                base_working_data = base_working_data.sort_index(ascending=True)
                return base_working_data
            else:
                traded_working_data.index = traded_working_data["Date"].values
                traded_working_data = traded_working_data[["Close"]]
                traded_working_data.columns = [["close"]]
                base_working_data["close"] = base_working_data["close"] / traded_working_data["close"]
                base_working_data = base_working_data.sort_index(ascending=True)
                return base_working_data

    def _get_historical_date_point_of_exchange(self,
                                               base_coin,
                                               traded_coin,
                                               end_datetime,
                                               exchange):
        end_date_timestamp = (end_datetime - Date(1970, 1, 1)).total_seconds()
        url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}&ts={}'\
                .format(base_coin.upper(), ','.join([traded_coin]).upper(), end_date_timestamp)

        page = requests.get(url)
        data = page.json()[base_coin][traded_coin]
        return data


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
               start_date = None, end_date = None,
               bar_size = None, bar_type = None, exch=None):
        if start_date is not None and end_date is not None:
            final_price = self.historical(base_coin, traded_coin, end_date, exchange = exch)
            initial_price = self.historical(base_coin, traded_coin, start_date, exchange = exch)
        else:
            # latest 1 bar of this size and diff close - open
            if bar_type == "d":
                bar_type = "h"
                bar_size = 24 * bar_size
            now = Date.now()
            data = self.historical(base_coin, traded_coin, now, bar_size = bar_size,
                                   bar_type = bar_type, num_points = 2, fields=["close", "open"])

            o = data.tail(1)["open"].values[0]
            c = data.tail(1)["close"].values[0]
            return (c/o-1) * 100

        return round((final_price / initial_price - 1) * 100, 2)
