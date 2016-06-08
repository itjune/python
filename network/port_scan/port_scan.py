import socket
import sys
from bs4 import BeautifulSoup
from urllib import request

def print_port(port, port_open, message):
    if message:
        if port_open:
            print('Port %d is open, application: %s' % (port, message))
        else:
            print('Port %d is close, application: %s' % (port, message))
    else:
        if port_open:
            print('Port %d is open' % (port))
        else:
            print('Port %d is close' % (port))

def port_app(soup, port):
    if soup.find('td', text=port):
        tcp = soup.find('td', text=port).next_sibling.next_sibling
        udp = tcp.next_sibling.next_sibling
        app = udp.next_sibling.next_sibling
        return ' '.join([tcp.text.strip(), udp.text.strip(), app.text.strip()]).replace('\n', ' ')
    else:
        return 'None'


def scan_ports(ip, port_list, timeout, desc=False):
    socket.setdefaulttimeout(timeout)
    if desc:
        data = request.urlopen('https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers')
        soup = BeautifulSoup(data, "html.parser")
    for port in port_list:
        if desc:
            desc = port_app(soup, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex((ip, port)) == 0:
            print_port(port, True, desc)
            sock.close()
        else:
            print_port(port, False, desc)

def get_ports(ports):
    ports = ports.split(',')
    port_list = []
    for item in ports:
        if '-' in item:
            start, stop = list(map(int, item.split('-')))
            for i in range(start, stop + 1):
                port_list.append(i)
        else:
            port_list.append(int(item))
    return port_list


if __name__ == '__main__':
    ip = input('Enter hostname/ip: ')
    if not ip:
        print('Please enter ip or hostname!')
        sys.exit(0)
    ports = input('Enter port range (ex. 80, 137-139): ')
    if not ports:
        print('Please enter port range!')
        sys.exit(0)
    timeout = input('Enter timeout: ')
    if not timeout:
        timeout = 5
    else:
        timeout = int(timeout)   
    try:
        ip = socket.gethostbyname(ip)
    except Exception as e:
        print("Can't resolve ip: %s" %(e))
        sys.exit(1)
    port_list = get_ports(ports)
    scan_ports(ip, port_list, timeout, True)
