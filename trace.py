# encoding utf-8

import json
import socket
import sys
import IPy
import geoip2.database
import draw_py3


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
        self.reciever.settimeout(1)

    def next_server(self):
        """ Connects to next server 1 hop away from current server (i.e. server[ttl + 1]) """
        if self.finished:
            # we have nothing to do, just return
            return

        # first job increment the ttl on the socket
        self.ttl += 1
        if self.ttl >= 20:
            self.finished = True
            j_ip.append(self.desternation)

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
        if IPy.IP.iptype(IPy.IP(address)) == 'PUBLIC' and address not in j_ip:
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

    ip_addr_list = ['www.bka.gv.at', 'www.belgium.be', 'www.government.bg', 'www.vlada.hr', 'www.cyprus.gov.cy',
                     'www.vlada.cz', 'denmark.dk', 'valitsus.ee', 'valtioneuvosto.fi', 'www.gouvernement.fr',
                     'www.bundesregierung.de', 'www.parliament.gr', 'www.kormany.hu', 'www.gov.ie', 'www.governo.it',
                     'www.mk.gov.lv', 'lrv.lt', 'www.gouvernement.lu', 'www.gov.mt', 'www.government.nl',
                     'www.premier.gov.pl', 'www.portugal.gov.pt', 'gov.ro', 'www.vlada.gov.sk', 'www.vlada.si',
                     'www.lamoncloa.gob.es', 'www.government.se', 'www.gov.uk']

    # ip_addr_list = ['www.bka.gv.at', 'www.belgium.be']

    trace_list = list()

    for addr in ip_addr_list:
        tracert = TraceRoute(addr)
        while not tracert.finished:
            tracert.next_server()
        if bool(j_ip):
            trace_list.append({'address': addr, 'hops': j_ip})
            j_ip = list()

    reader = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')
    for key, i in enumerate(trace_list):
        for k, j in enumerate(i['hops']):
            print(j)
            response = reader.city(j)
            trace_list[key]['hops'][k] = {'ip': j, 'lat': response.location.latitude, 'lon': response.location.longitude}
    # print json.dumps(trace_list, separators=(',', ':'))
    draw_py3.generate(json.dumps(trace_list, separators=(',', ':')))
    # print json.dumps(trace_list, indent=4, separators=(',', ':'))
