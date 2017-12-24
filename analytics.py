import pandas as pd
import numpy as np
import json
from datetime import date

def cleaned_dataset():
    data = pd.read_csv(
        'coin_data_cleaned.csv',
        header=0,
        low_memory=False,
        encoding='utf-8-sig',
        delimiter=','
    )
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Market-Cap'] = pd.to_numeric(data['Market-Cap'], errors='coerce')
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')
    data = data.drop_duplicates()
    return data


def getCoin(dataset, coin):
    return dataset[(dataset['Coin'] == coin)]

def getDates(dataset, startDate, endDate):
    return dataset[((dataset['Date'] >= startDate) & (dataset['Date'] <= endDate))]

def getDate(dataset, date):
    return dataset[(dataset['Date'] == date)]

def getSorted(data, column, asc = False):
    return data.sort_values(by=column, ascending=asc).dropna()

def getClose(data, coin, date):
    dataDate = getDate(data, date)
    dataCoin = getCoin(dataDate, coin)
    return float(dataCoin["Close"].values[0])

def top10_by_market_cap(top100):
    top10 = top100[top100['Date'] == '2017-12-18'].sort_values('Market-Cap', ascending=False)
    print(top10[['Coin', 'Market-Cap']][:10])
    top10[['Coin', 'Market-Cap']][:10].to_csv('top10_marketcap.csv')
    print(top10[['Coin', 'Market-Cap']][-10:])
    top10[['Coin', 'Market-Cap']][-10:].to_csv('bottom10_market_cap.csv')

def top_by_market_cap(dataset, date='2017-12-18'):
    dataset = dataset[top100['Date'] == date].sort_values('Market-Cap', ascending=False)
    return dataset

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


# dataset = cleaned_dataset()
#top10_by_market_cap(dataset)
# current = get_historical_data(dataset, 'litecoin', '2017-12-16', '2017-12-18')

# hist = get_historical_data(dataset, 'litecoin', '2017-12-01', '2017-12-01')
# current['diff'] = (current['Close'] - hist['Close'].values[0]) / hist['Close'].values[0]
# print(current)

#filtered_data(dataset, per_exchange_currencies(['Poloniex', 'Bitfinex']))
