import requests
import datetime
import pandas as pd
from datetime import datetime as Date

def historical( base_coin,
                traded_coin,
                start_date,
                end_date,
                freq = "daily",
                size = 1,
                num_points = None,
                exchange = ''):
    if freq == "hourly":
        return hourly_price_historical(base_coin, traded_coin, num_points, size, exchange)
    elif freq == "minute":
        return minute_price_historical(base_coin, traded_coin, num_points, size, exchange)
    elif freq == "daily":
        return daily_price_historical(base_coin, traded_coin, num_points, size, exchange)

def current(base_coin, traded_coin, exchange=''):
    return price_current(base_coin, [traded_coin], exchange)

def daily_price_historical( symbol,
                            comparison_symbol,
                            limit,
                            aggregate,
                            exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), aggregate)
    if exchange:
        url += '&e={}'.format(exchange)

    if limit is None:
        url += '&allData=true'
    else:
        url += '&limit={}'.format(limit)

    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df.index = [Date.fromtimestamp(d) for d in df.time]
    return df

def hourly_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df.index = [Date.fromtimestamp(d) for d in df.time]
    return df

def minute_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def price_current(symbol, comparison_symbols=['USD'], exchange=''):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    return data
