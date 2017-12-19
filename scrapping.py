import requests
import pandas as pd
from bs4 import BeautifulSoup

page = requests.get('https://coinmarketcap.com/historical/20171217')

soup = BeautifulSoup(open("all_cryptos.html"), 'html.parser')
table_rows = soup.find_all('tr')

coins = []

for i in range(1, len(table_rows)):
    coins.append(table_rows[i].find_all('a')[0]['href'].split('/')[2])



df = pd.DataFrame(coins, columns=['Coins'])
df.to_csv('coins.csv')

