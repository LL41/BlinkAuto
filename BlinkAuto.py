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

def find_devices(target_ips):
    icmp_request = IP(dst=target_ips)/ICMP()
    icmp_replies, _ = sr(icmp_request, timeout=2, verbose=False)
    return icmp_replies

def monitor_network(lost_device_time,currently_armed,target_ips):
    #Check for certain devices on network.
    icmp_replies = find_devices(target_ips)
    #If devices are found, print out which devices are found and set lost_device_time to 0.
    if icmp_replies:
        for icmp_reply in icmp_replies:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print(f"ICMP reply received from {icmp_reply[1].src}")
            lost_device_time = 0
            if currently_armed == True:
            #Disarm camera if it was last armed by the script.
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
        #If the device was not found add time to the lost_device_time counter.
        lost_device_time += 1
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Time without connection: '+ str(lost_device_time))

    #Check if devices have been offline for (lost_device_time*time.sleep())
    #If the device has been offline for the set limit, arm the system.
    if (lost_device_time == 20) and (currently_armed == False):
        arm_blink(True)
        print('Armed')
        currently_armed = True
    else:
        pass

    time.sleep(3)

target_ips = ['IP_ADDRESS']

while True:
    monitor_network(0,False,target_ips)