import pandas as pd
import numpy as np
import json
from datetime import date

def cleaned_dataset():
    top100 = pd.read_csv(
        'top100_coin_data_cleaned.csv',
        header=0,
        low_memory=False, 
        encoding='utf-8-sig',
        delimiter=','
    )
    top100['Date'] = pd.to_datetime(top100['Date'], errors='coerce')
    top100['Market-Cap'] = pd.to_numeric(top100['Market-Cap'], errors='coerce')
    top100['Volume'] = pd.to_numeric(top100['Volume'], errors='coerce')

    return top100

def top10_by_market_cap(top100):
    top10 = top100[top100['Date'] == '2017-12-18'].sort_values('Market-Cap', ascending=False)
    print(top10[['Coin', 'Market-Cap']][:10])
    top10[['Coin', 'Market-Cap']][:10].to_csv('top10_marketcap.csv')
    print(top10[['Coin', 'Market-Cap']][-10:])
    top10[['Coin', 'Market-Cap']][-10:].to_csv('bottom10_market_cap.csv')

def get_historical_data(top100, ticker, start, end):
    return top100[
        (top100['Coin'] == ticker) & 
        (top100['Date'] >= start) &
        (top100['Date'] <= end)][['Date', 'Volume', 'Close', 'Market-Cap']]

def per_exchange_currencies(exchange_names):
    exchanges = json.load(open('dict.json'))
    all_currencies = set()
    for name in exchange_names:
        all_currencies = all_currencies | set(exchanges[name])

    return all_currencies

# get all from top 100 that are traded at the exchanges passed in as parameter
def filtered_data(top100, exchange_names):
    top100 = top100[top100['Coin'].isin(exchange_names)]
    top100 = top100[top100['Date'] == '2017-12-18']

    print(top100)


dataset = cleaned_dataset()
#top10_by_market_cap(dataset)
# current = get_historical_data(dataset, 'litecoin', '2017-12-16', '2017-12-18')

# hist = get_historical_data(dataset, 'litecoin', '2017-12-01', '2017-12-01')
# current['diff'] = (current['Close'] - hist['Close'].values[0]) / hist['Close'].values[0]
# print(current)

#filtered_data(dataset, per_exchange_currencies(['Poloniex', 'Bitfinex']))
