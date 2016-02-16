#!/usr/bin/python3

import socket
import time
import argparse

def traceroute(target):
    """
        python3 implementation of traceroute
    """

    addr = socket.gethostbyname(target)
    port = 33434
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    num_hops = None

    print("\nBeginning traceroute %s ( %s )\n" % (target, addr))

    start_time = time.time()

    for ttl in range(1,31):
        num_hops = ttl
        hop_etime = None

        recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        
        send.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv.settimeout(1)
        recv.bind(("", port))

        hop_stime = time.time()
        send.sendto(bytes("", 'UTF-8'), (target, port))

        hop_addr = None
        hop_name = None

        try:
            _, curr_addr = recv.recvfrom(512)
            hop_etime = time.time()
            hop_addr = curr_addr[0]
            try:
                hop_name = socket.gethostbyaddr(hop_addr)
            except socket.error:
                hop_name = hop_addr

            if type(hop_name) is not tuple:
                hop_name = ("*")

        except socket.error:
            pass
        except socket.timeout:
            hop_etime = time.time()

        finally:
            send.close()
            recv.close()
            if hop_etime == None:
                hop_etime = time.time()

            if hop_name == None:
                hop_name = ("*")
                hop_addr = "Timeout!"

        print("%s\t%s ( %s )\t%.2fms" % (ttl, hop_name[0], hop_addr,(hop_etime - hop_stime) * 1000))
        if hop_addr == addr:
            break
    
    end_time = time.time()
    print("\nTraceroute to %s completed..." % target)
    print("Hops : %s\tTotal time: %.2fms" % (str(num_hops), (end_time - start_time) * 1000))
    if num_hops == 30:
        print("MAX HOPS Reached\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Hostname or IP address to trace to")
    args=parser.parse_args()

    traceroute(args.target)