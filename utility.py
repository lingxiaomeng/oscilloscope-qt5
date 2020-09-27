import socket, os, re


def get_local_net():
    # 获取主机名
    hostname = socket.gethostname()
    # 获取主机的局域网ip
    localip = socket.gethostbyname(hostname)
    localipnums = localip.split('.')
    localipnums.pop()
    localipnet = '.'.join(localipnums)
    return localipnet


def ip_auto_detect():
    ips = os.popen("arp -a")
    data = ips.read()
    local_ip = get_local_net()
    ips = re.findall(r'' + local_ip + '.\d+', data)
    for ip in ips:
        if 1 < int(ip.split('.')[3]) < 255:
            return ip


