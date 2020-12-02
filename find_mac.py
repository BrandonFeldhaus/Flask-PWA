from scapy.all import *
from scapy.layers.l2 import ARP, Ether
#import psutil
import subprocess
#import netifaces
import requests

def get_default_gateway():
    route_default_result = str(subprocess.check_output(["route", "get", "default"]))
    start = 'gateway: '
    end = '\\n'
    if 'gateway' in route_default_result:
        return (route_default_result.split(start))[1].split(end)[0]

def get_mac_details(mac_address):

    # Use an API to get the vendor details
    url = "https://api.macvendors.com/"

    # Use get method to fetch details
    response = requests.get(url+mac_address)
    if response.status_code != 200:
        pass
        #raise Exception("[!] Invalid MAC Address!")
    return response.content.decode()

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
        clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor' : get_mac_details(str(received.hwsrc))})# "vendor": get_mac_details(received.hwsrc)})
    #print("Vendor: ", get_mac_details("b8:f8:53:1c:59:93"))
    # print clients
    print("Available devices in the network:")
    print("IP" + " " * 18 + "MAC" + " " * 18 + "Vendor")
    for client in clients:
        print("{:16}    {}      {}".format(client['ip'], client['mac'], client['vendor']))

    return clients

def main():
    get_ips('192.168.0.1/24')
    #gws = netifaces.gateways()
    #gateway = gws['default'][netifaces.AF_INET][0]
    #subnet = gateway+'/24'
    #print("Gateway name:", get_default_gateway(), '\nGateway IP:', subnet, '\n')
    #return get_ips(subnet)


if __name__ == '__main__':
    main()
