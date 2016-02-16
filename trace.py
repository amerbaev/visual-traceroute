# encoding utf-8

import json
import socket
import sys
import IPy


class TraceRoute(object):
    BADDR = "0.0.0.0"  # default bind address - (all IPs)
    PORT = 33434  # default port
    ICMP = socket.getprotobyname('icmp')
    UDP = socket.getprotobyname('udp')

    desternation = ""
    ttl = 0  # we inrecement this by one each time

    # sockets
    reciever = None
    sender = None

    # finished?
    finished = False

    def __init__(self, desternation):

        try:
            self.desternation = socket.gethostbyname(desternation)
        except socket.error:
            print "Unavailable to retrieve host by name"
            self.finished = True

        self.reciever = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.ICMP)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, self.UDP)

        # bind to reciever so we can listen for replies
        self.reciever.bind((self.BADDR, self.PORT))
        self.reciever.settimeout(5)

    def next_server(self):
        """ Connects to next server 1 hop away from current server (i.e. server[ttl + 1]) """
        if self.finished:
            # we have nothing to do, just return
            return

        # first job increment the ttl on the socket
        self.ttl += 1
        self.sender.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)

        self.sender.sendto("", (self.desternation, self.PORT))

        try:
            current_server = self.reciever.recvfrom(512)[1][0]  # get 512 bytes from the reciever
            self.display(current_server)
        except socket.error:
            print "***"
            return

        if current_server == self.desternation:
            self.finished = True

    def display(self, address):
        """ Gets the hostname (if we can) and displays """
        global j_ip
        if IPy.IP.iptype(IPy.IP(address)) == 'PUBLIC':
            j_ip.append(address)

        try:
            name = socket.gethostbyaddr(address)[0]
            print "%s" % (address)
        except socket.error:
            # we couldn't - we'll just tell them the IP address
            print "%s" % (address)

    def __del__(self):
        """ Be good and close our sockets """
        try:
            self.reciever.close()
        except socket.error:
            # already closed
            pass

        try:
            self.sender.close()
        except socket.error:
            # already closed
            pass


if __name__ == "__main__":
    # lets get the address from the commandline args
    j_ip = list()

    ip_addr_list = ['78.41.145.34', '193.191.245.244', '212.122.160.100', '185.20.29.90', '212.31.118.26',
                    '89.233.150.22', '213.174.72.92', '213.184.53.253', '131.207.14.37', '185.13.160.61',
                    '46.243.126.120', '195.251.32.78', '195.228.130.17', '54.154.87.28', '195.66.10.19',
                    '212.70.163.182', '195.182.89.166', '176.34.240.169', '217.71.177.230', '178.22.85.24',
                    '46.28.14.4', '192.230.78.192', '85.120.75.150', '195.49.188.138', '84.39.223.151',
                    '193.146.141.234', '88.221.133.41', '23.235.43.144']

    trace_list = list()

    for addr in ip_addr_list:
        tracert = TraceRoute(addr)
        while not tracert.finished:
            tracert.next_server()
        if bool(j_ip):
            trace_list.append({'address': addr, 'hops': j_ip})
            j_ip = list()

    print json.dumps(trace_list, indent=4, separators=(',', ':'))
