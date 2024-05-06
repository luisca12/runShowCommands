from netmiko import ConnectHandler
from functions import *
from log import *
from strings import *
from auth import *

import os
import traceback
import re

shRun = "show run"
shHostname = "show run | i hostname"

def showRun(validIPs, username, netDevice):
    # This function is to take a show run
    
    for validDeviceIP in validIPs:
        try:
            validDeviceIP = validDeviceIP.strip()
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 120,
                'session_log': 'netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                sshAccess.enable()
                shHostnameOut = sshAccess.send_command(shHostname)
                authLog.info(f"User {username} successfully found the hostname {shHostnameOut}")
                shHostnameOut = shHostnameOut.replace('hostname', '')
                shHostnameOut = shHostnameOut.strip()
                shHostnameOut = shHostnameOut + "#"

                with open(f"{validDeviceIP}_showRun.txt", "a") as file:
                    file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                    authLog.info(f"User {username} is now running commands at: {validDeviceIP}")

                    print(f"INFO: Taking a {shRun} for device: {validDeviceIP}")
                    shRunOut = sshAccess.send_command(shRun)
                    print(f"INFO: {shRun} taken for device: {validDeviceIP}")
                    authLog.info(f"Automation successfully ran the command: {shRun}")
                    file.write(f"{shRunOut}")

        except Exception as error:
            print(f"An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.debug(traceback.format_exc(),"\n")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} connected to {validDeviceIP} got an error.\n")
        
        finally:
            print("Outputs and files successfully created.\n")
            print("For any erros or logs please check authLog.txt\n")