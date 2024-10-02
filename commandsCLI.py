from netmiko import ConnectHandler
from log import authLog
from functions import failedDevices, logInCSV

import traceback
import os

shCommand = ""
shHostname = "show run | i hostname"

def showCommands(validIPs, username, netDevice, shCommand):
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
                'session_log': 'Outputs/netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"INFO: Connecting to device {validDeviceIP}...")
            authLog.info(f"Connecting to device {validDeviceIP}")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                try:
                    authLog.info(f"Connected to device: {validDeviceIP}")
                    sshAccess.enable()
                    shHostnameOut = sshAccess.send_command(shHostname)
                    authLog.info(f"User {username} successfully found the hostname {shHostnameOut} for device: {validDeviceIP}")
                    shHostnameOut = shHostnameOut.split(' ')[1]
                    shHostnameOut = shHostnameOut + "#"

                    shCommandOut = sshAccess.send_command(shCommand)

                    # with open(f"{validDeviceIP}_showRun.txt", "a") as file:
                    #     file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                    #     authLog.info(f"User {username} is now running commands at: {validDeviceIP}")
                    #     print(f"INFO: Taking a {shCommand} for device: {validDeviceIP}")
                    #     print(f"INFO: {shCommand} taken for device: {validDeviceIP}")
                    #     authLog.info(f"Automation successfully ran the command: {shCommand}")
                    #     file.write(f"{shCommandOut}")

                    print("Outputs and files successfully created.\n")
                    print("For any erros or logs please check authLog.txt\n")

                except Exception as error:
                    print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
                    authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
                    authLog.error(traceback.format_exc(),"\n")
                    failedDevices(username,validDeviceIP,error)
                    
        except Exception as error:
            print(f"ERROR: An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.error(traceback.format_exc(),"\n")
            failedDevices(username,validDeviceIP,error)   