import subprocess
import platform
import socket
from scapy.all import *
os_name = platform.system()
gateway = None
def gethostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"
def scanning(ip_range):
    arp=ARP(pdst=ip_range)
    ether=Ether(dst="ff:ff:ff:ff:ff:ff")
    packet=ether/arp
    result=srp(packet,timeout=2,verbose=0)[0]
    devices=[]
    for sent,received in result:
        ip=received.psrc
        hostname=gethostname(ip)
        devices.append({"ip":ip,"hostname":hostname})
    return devices
if os_name == "Windows":
    result = subprocess.run('netsh wlan show interfaces', capture_output=True, text=True, shell=True)
    for line in result.stdout.splitlines():
        if "SSID" in line and "BSSID" not in line:
            ssid = line.partition(':')[2].strip()
            print(f"connected network name: {ssid}")
elif os_name == "Linux":
    result = subprocess.run('iwgetid -r', capture_output=True, text=True, shell=True)
    ssid = result.stdout.strip()
    print(f"connected network name: {ssid}")
gateway = input("Please enter the gateway/router IP address: ").strip()
if gateway:
    print(f"IP address (network gateway): {gateway}")
else:
    print("No gateway entered")
results=scanning(f"{gateway}/24")
for device in results:
    print(device)
inp_ip=input("Please enter the IP address: ")
if os_name=="Windows":
    result=subprocess.run("ping -n 1 -w 1000 "+inp_ip,capture_output=True,text=True,shell=True)
    print(result.stdout)
elif os_name=="Linux":
    result=subprocess.run("ping -c 1 -w 1000 "+inp_ip,capture_output=True,text=True,shell=True)
    print(result.stdout)