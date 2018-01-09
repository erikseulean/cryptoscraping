import requests
import concurrent.futures
import asyncio
import time
import json
import pandas as pd
from multiprocessing import Pool, cpu_count
from collections import defaultdict
from bs4 import BeautifulSoup

def get_url(coin):
    url = "https://coinmarketcap.com/currencies/{coin}/#markets"
    url = url.format(coin=coin)

    return url

def get_exchanges_for_coin(coin):

    contents = requests.get(get_url(coin)).content

    soup = BeautifulSoup(contents, 'html.parser')

    table = soup.find("table", {"id": "markets-table"})
    table_rows = table.find_all('tr')
    unique_exchanges = set()

    for i in range(1, len(table_rows)):
        unique_exchanges.add(table_rows[i].find_all('td')[1].find_all('a')[0].text)
    return coin, unique_exchanges


async def scrap_exchanges():
    coins = pd.DataFrame.from_csv('crypto/data/coins.csv')

    data = defaultdict(lambda:[])
    chunks = [coins[i: i + 5] for i in range(0, len(coins), 5)]
    print('nr chunks ', len(chunks))
    for chunk in chunks[0:10]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [loop.run_in_executor(executor, get_exchanges_for_coin, coin.split(":")[0]) for coin in chunk["Coins"]]

            for future in futures:
                coin, exchanges = await future
                for exchange in exchanges:
                    data[exchange].append(coin)
        time.sleep(3)

    print("done")
    # json.dump(data, open('crypto/data/dict.json', 'w'))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap_exchanges())
