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
        if IPy.IP.iptype(address) == 'PUBLIC':
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
    if not bool(sys.argv[1]):
        # nothing been specified
        print "You need to give an address"
        print "%s <server>" % sys.argv[0]
        sys.exit()  # we can't do anything.

    tracert = TraceRoute(sys.argv[1])
    while not tracert.finished:
        tracert.next_server()

    if bool(j_ip):
        print json.dumps( {'address': sys.argv[1], 'hops':j_ip}, indent=4, separators=(',', ':') )
    else:
        print "Hops list is empty"
