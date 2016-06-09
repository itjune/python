from bs4 import BeautifulSoup
from urllib import request

ip = input('Enter ip: ')
full = input('Do you need more info [no]: ')

data = request.urlopen('https://db-ip.com/' + ip)
soup = BeautifulSoup(data, "html.parser")


if full:
    for i in range(len(soup.find_all('th'))):
        if soup.find_all('th')[i].text != 'Local time':
            print(soup.find_all('th')[i].text, '\t',
                  soup.find_all('td')[i].text.strip())
else:
    for i in range(len(soup.find_all('th'))):
        if soup.find_all('th')[i].text == 'Country':
            print(soup.find_all('th')[i].text, '\t',
                  soup.find_all('td')[i].text.strip())
            break
    
