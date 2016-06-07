import socket
import sys

def scan_ports(ip, port_list, timeout):
    socket.setdefaulttimeout(timeout)
    for port in port_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex((ip, port)) == 0:
            print('Port %d is open' % (port))
            sock.close()
        else:
            print('Port %d is close' % (port))

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
    scan_ports(ip, port_list, timeout)
