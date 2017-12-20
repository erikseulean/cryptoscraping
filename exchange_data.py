import requests
import json
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup

def get_exchanges(coin):
    url = "https://coinmarketcap.com/currencies/{coin}/#markets"
    url = url.format(coin=coin)

    page = requests.get(url)
    contents = page.content

    soup = BeautifulSoup(contents, 'html.parser')
    
    table = soup.find("table", {"id": "markets-table"})
    table_rows = table.find_all('tr')
    unique_exchanges = set()

    for i in range(1, len(table_rows)):
        unique_exchanges.add(table_rows[i].find_all('td')[1].find_all('a')[0].text)
    return unique_exchanges

def store_exchanges():
    coins = pd.DataFrame.from_csv('coins.csv')
    
    data = defaultdict(lambda:[])

    for coin in coins['Coins'][0:100]:
        exchange = get_exchanges(coin)
        for exch in exchange:
            data[exch].append(coin)

    json.dump(data, open('dict.json', 'w'))   
    
store_exchanges()


    

