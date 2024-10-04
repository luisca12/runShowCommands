from netmiko import ConnectHandler
from log import authLog
from functions import failedDevices, logInCSV, filterFilename

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

                    authLog.info(f"Command input by the user:{username}, command:{shCommand}")
                    print(f"INFO: Running command:{shCommand}, on device {validDeviceIP}")
                    shCommandOut = sshAccess.send_command(shCommand)
                    authLog.info(f"Automation successfully run the command: {shCommand} on device: {validDeviceIP}")
                    authLog.info(f"{shHostnameOut}{shCommand}\n{shCommandOut}")
                    print(f"INFO: Command successfully executed\n{shHostnameOut}{shCommand}\n{shCommandOut}")

                    filename = filterFilename(shCommand)
                    authLog.info(f"This is the filename:{filename}")

                    with open(f"Outputs/{filename} for device {validDeviceIP}.txt", "a") as file:
                        file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                        file.write(f"{shHostnameOut}{shCommand}\n{shCommandOut}")
                        authLog.info(f"File:{file} successfully created")

                    print("INFO: Outputs and files successfully created.")
                    print("INFO: For any erros or logs please check authLog.txt in logs")

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