import subprocess
import platform
os_name=platform.system()
if os_name=="Windows":
    result=subprocess.run('netsh wlan show interfaces',capture_output=True,text=True,shell=True)
    for line in result.stdout.splitlines():
        if "SSID" in line and "BSSID" not in line:
            ssid=line.partition(':')[2].strip()
            print(f"connected network name:{ssid}")
elif os_name=="Linux":
    result=subprocess.run('iwgetid -r',capture_output=True,text=True,shell=True)
    ssid=result.stdout.strip()
    print(f"connected network name:{ssid}")
try:
    if os_name=="Windows":
        result=subprocess.run("ipconfig",capture_output=True,text=True,shell=True)
        lines=result.stdout.splitlines()
        for i,line in enumerate(lines):
            if "Default Gateway" in line:
                gateway=line.split(':')[-1].strip()
                if gateway and len(gateway)<=15:
                    break
                else:
                    if i+1<len(lines):
                        next_line=lines[i+1].strip()
                        if next_line and len(next_line)<=15:
                            gateway=next_line
                            break
    elif os_name=="Linux":
        result=subprocess.run("ip route",capture_output=True,text=True,shell=True)
        for line in result.stdout.splitlines():
            if line.startswith('default'):
                gateway=line.split()[2]
                break
except Exception as e:
    print(f"Error getting gateway:{e}")
if gateway:
    print(f"IP address(network gateway) :{gateway}")
else:
    print("No gateway found")

