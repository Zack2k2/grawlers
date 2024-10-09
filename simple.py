from curl_cffi import requests
from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
res = requests.get(url,impersonate='chrome')


soup = BeautifulSoup(res.text, 'html.parser')

for link in soup.find_all('a'):
    if 'href' in link.attrs:
        print(link.attrs['href'])
