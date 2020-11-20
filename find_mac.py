from scapy.all import *
from scapy.layers.l2 import ARP, Ether
#import psutil


def get_ips(target):
    print("target:", target)
    target_ip = target
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_ip)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether/arp

    result = scapy.all.srp(packet, timeout=3, verbose=0)[0]
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    # print clients
    print("Available devices in the network:")
    print("IP" + " " * 18 + "MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))

    return clients


# just me testing another service, ignore for now
def psu_test():
    # print(psutil.net_connections(kind='inet'))
    pass


def main():
    get_ips('192.168.0.1/24')


if __name__ == '__main__':
    main()
    # a list of cli