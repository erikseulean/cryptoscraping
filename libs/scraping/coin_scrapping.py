import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrap_coins():

    soup = BeautifulSoup(open("data/all_cryptos.html"), 'html.parser')
    table_rows = soup.find_all('tr')

    coins = []

    for i in range(1, 10):
        coins.append( table_rows[i].find_all('a')[0]['href'].split('/')[2] + ":" + \
                      table_rows[i].find_all('a')[0].text)

    df = pd.DataFrame(coins, columns=['Coins'])
    df.to_csv('data/coins.csv')
    print('loaded all coins into coins.csv')


def scrap_at_date(path, mode='a', header = False):

    page = requests.get('https://coinmarketcap.com{path}')
    contents = page.content