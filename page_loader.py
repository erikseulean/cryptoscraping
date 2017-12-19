import requests

# all currencies
page = requests.get('https://coinmarketcap.com/historical/20171217')
contents = page.content


with open("all_cryptos.html", "wb") as text_file:
    text_file.write(contents)

print('done')