from crypto.data.loader import cleaned_dataset
from crypto.analytics.analytics import get_historical_data
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def get_trends(coin):
    trends = pd.read_csv(
        'crypto/data/coin_trends.csv',
        header=0,
        low_memory=False, 
        encoding='utf-8-sig',
        delimiter=','
    )

    return trends[trends['Coin'] == coin][['Date', 'Trend']]

def close_prices(coin):
    data = cleaned_dataset()
    data = get_historical_data(cleaned_dataset(), coin, '2017-09-21', '2018-01-09')
    min_value = data['Close'][data['Close'].idxmin()]
    max_value = data['Close'][data['Close'].idxmax()]
    data['Close'] = (data['Close'] - min_value)/(max_value - min_value) * 100
    return data[['Date', 'Close']]
    

def plot_correlation(coin):
    prices = close_prices(coin)
    trend = get_trends(coin)
    trend['MA'] = pd.rolling_mean(trend['Trend'], window=3)
    plt.plot(prices['Date'],prices['Close'], color='red')
    plt.plot(trend['Date'], trend['MA'], color='purple')
    plt.title(coin)
    plt.show()
    
