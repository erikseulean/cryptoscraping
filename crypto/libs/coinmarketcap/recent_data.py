import requests
import json

def get_current_values():
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=10000'

    response = requests.get(url)
    return { elem['id']:elem for elem in json.loads(response.content.decode('utf8')) }
