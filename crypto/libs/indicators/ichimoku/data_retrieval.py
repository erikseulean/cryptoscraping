import json
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def get_prices_hour_buckets(coin):
    url = "https://min-api.cryptocompare.com/data/histohour?fsym={coin}&tsym=BTC&limit=10000&aggregate=1&e=CCCAGG"
    url = url.format(coin=coin)

    data = json.loads(requests.get(url).content.decode("utf-8"))["Data"]
    data = pd.DataFrame(data)
    data['close'] = pd.to_numeric(data['close'])
    data['high'] = pd.to_numeric(data['high'])
    data['low'] = pd.to_numeric(data['low'])
    data['time'] = pd.to_numeric(data['time'])
    data['time'] = pd.to_datetime(data['time'], errors='coerce', unit='s')
    data['rollingMax'] = data['high'].rolling(center=False, window=20).max()
    data['rollingMin'] = data['low'].rolling(center=False, window=20).min()
    data['kijun'] = (data['high'] + data['low'])/2
    data.set_index(['time'],inplace=True)
    data = data[20:]
    print(data)

get_prices_hour_buckets('WTC')