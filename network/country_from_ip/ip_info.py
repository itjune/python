from bs4 import BeautifulSoup
from urllib import request

ip = input('Enter ip: ')

data = request.urlopen('https://db-ip.com/' + ip)
soup = BeautifulSoup(data, "html.parser")
soup.find_all('td')
