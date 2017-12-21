from multiprocessing import Pool, cpu_count
from pytrends.request import TrendReq
import pandas as pd

def get_trends(coin_term, mode='a', header=False):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(coin_term, cat=0, timeframe='today 3-m', geo='', gprop='')

    result = pytrends.interest_over_time()
    result.insert(loc=0, column='Coin', value='-'.join(coin_term))
    result.drop('isPartial', axis=1, inplace=True)
    result.reset_index(level=0, inplace=True)

    result = result.iloc[:,0:3]
    result.columns = ['Date', 'Coin', 'Trend']

    with open('coin_trends.csv', mode) as f:
        result.to_csv(f, index=False, header=header)


def get_all_trends():
    df = pd.DataFrame.from_csv('coins.csv')
    
    coins = df['Coins'][0:100].tolist()
    coins = [str(elem).split('-') for elem in coins]

    get_trends(coins[0], mode='w', header=True)

    # running in parallel has a glitch? 
    # eventually google api is trottling something?

    for coin in coins:
        get_trends(coin)
    
    # with Pool(processes=cpu_count()) as pool:
    #     pool.map(get_trends, coins[1:100])
