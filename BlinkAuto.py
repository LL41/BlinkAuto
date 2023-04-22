import logging
import os
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import time
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth

def arm_blink(armed):
    username = 'YOUR_USERNAME'
    password = 'YOUR_PASSWORD'
    blink = Blink()
    auth = Auth({"username": f'{username}', "password": f'{password}'})
    blink.auth = auth
    blink.start()
    blink.sync["YOUR_SYNCMODULE_NAME"].arm = armed

target_ips = ['IP_ADDRESS']

def find_devices(target_ips):
    icmp_request = IP(dst=target_ips)/ICMP()

    icmp_replies, _ = sr(icmp_request, timeout=2, verbose=False)

    return icmp_replies

lost_device_time = 0
currently_armed = False
while True:
    icmp_replies = find_devices(target_ips)
    if icmp_replies:
        for icmp_reply in icmp_replies:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print(f"ICMP reply received from {icmp_reply[1].src}")
            lost_device_time = 0
            if currently_armed == True:
                try:
                    print('Disarming')
                    arm_blink(False)
                    currently_armed = False
                except:
                    print('Disarm failed. Trying again.')
                    time.sleep(60)
                    arm_blink(False)
                    currently_armed = False
                finally:
                    pass

            else:
                pass

    else:
        lost_device_time += 1
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Time without connection: '+ str(lost_device_time))

#Check if devices have been offline for more than 5 minutes. (20)
    if (lost_device_time == 20) and (currently_armed == False):
        arm_blink(True)
        print('Armed')
        currently_armed = True
    else:
        pass

    time.sleep(3)