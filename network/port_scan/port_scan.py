import socket

def scan_ports(ip, port_list, timeout=10):
    socket.setdefaulttimeout(timeout)
    for port in port_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        if sock:
            print('Port %d is open' % (port))
            sock.close()
        else:
            print('Port %d is close' % (port))
    
        

