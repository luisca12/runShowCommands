from utils import mkdir


import os

def main():
    mkdir()
    from strings import greetingString, menuString, inputErrorString
    greetingString()
    from auth import Auth
    from functions import checkIsDigit, checkYNInput
    from commandsCLI import showCommands
    from log import authLog
    
    validIPs, username, netDevice = Auth()

    while True:
        shCommand = input("Please input the complete show command to run:")
        menuString(validIPs, username, shCommand)
        selection = input("\nPlease choose the option that you want: ")
        if checkIsDigit(selection):
            if selection == "1":
                # This option will take a show run
                showCommands(validIPs, username, netDevice, shCommand)
                os.system("CLS")
                print(f"INFO: Successfully run {shCommand} on {validIPs}\n")
                selection1 = input(f"Do you want to run another show command? (y/n):")
                while not checkYNInput(selection1):
                    print("Invalid input. Please enter 'y' or 'n'.\n")
                    authLog.error(f"User tried to choose a CSV file but failed. Wrong option chosen: {selection1}")
                    selection1 = input("Do you want to run another show command? (y/n):")
                if selection1 == "n":
                    authLog.info(f"User {username} disconnected from the devices {validIPs}")
                    authLog.info(f"User {username} logged out from the program.")
                    print(f"INFO: Successfully logged out of the program and devices")
                    break

            if selection == "2":
                authLog.info(f"User {username} disconnected from the devices {validIPs}")
                authLog.info(f"User {username} logged out from the program.")
                break
        else:
            authLog.error(f"Wrong option chosen {selection}")
            inputErrorString()
            os.system("PAUSE")

if __name__ == "__main__":
    main()