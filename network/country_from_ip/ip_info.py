from bs4 import BeautifulSoup
from urllib import request

ip = input('Enter ip: ')

data = request.urlopen('https://db-ip.com/' + ip)
soup = BeautifulSoup(data, "html.parser")


for i in range(len(soup.find_all('th'))):
	print(soup.find_all('th')[i].text, '\t',
	      soup.find_all('td')[i].text.strip())
