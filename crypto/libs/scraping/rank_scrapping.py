import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com{path}"

def scrap_rankings():

    page = requests.get(url.format(path='/historical'))
    contents = page.content

    soup = BeautifulSoup(contents, 'html.parser')
    ul = soup.find_all('ul', {'class': 'list-unstyled'})

    return [elem.find_all('li')[0].find_all('a')[0]['href'] for elem in ul if isinstance(elem.find_all('li'), list)]

def scrap_rank(path):

    page = request.get(url.format(path=path))
    contents = page.content

    soup = BeautifulSoup(contents, 'html.parser')
