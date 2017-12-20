import requests

# all currencies
def load():
    page = requests.get('https://coinmarketcap.com/all/views/all/')
    contents = page.content


    with open("all_cryptos.html", "wb") as text_file:
        text_file.write(contents)

    print('saved html source to all_cryptos.html')