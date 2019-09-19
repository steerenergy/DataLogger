# Main Menu - Initialised by UI.py
# First gives option for user to select the logger hostname and redirects all error messages to 'uiError.log'
# Then. this creates the main menu linking to other imported modules

# Import local python files for operation
import common
import logCtrl
import about
import processData
import generalSettings
import ctypes
from datetime import datetime
import logging
import sys
import comms


# Title printed on program start
def init():
    # Start Error Logging
    errorLoggingSetup()
    # Redirect all stderr to text file - comment the next line out to make errors appear on the console
    sys.stderr.write = stderrRedirect
    version = "1.1.2 Alpha"
    # Set Windows Title
    welcomeMessage = "Steer Energy Data Logger (Version {})".format(version)
    ctypes.windll.kernel32.SetConsoleTitleW(welcomeMessage)
    print(welcomeMessage)
    print("-" * len(welcomeMessage))
    print("Read User Manual before First Use - Use keyboard for input, pressing 'Enter' to confirm input\n")
    # Initiate hostname selection - welcomeMessage sent so window title can be updated
    comms.init(welcomeMessage)
    # Initiate main menu
    main()


# Setup error logging
def errorLoggingSetup():
    # Used to set logger
    errorLogger = logging.getLogger('error_logger')
    # Select min level of severity to log
    errorLogger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('uiError.log')
    fh.setLevel(logging.INFO)
    errorLogger.addHandler(fh)
    # Print Top Line to make it easy to identify new instance of program
    errorLogger.info("\n\n{}\nNEW INSTANCE OF UI @ {}\n{}\n".format('-' * 75, datetime.now(), '-' * 75))


# Function called every time a line of an error is written to sys.stderr
# Redirects them from the (invisible) console to the log file
def stderrRedirect(buf):
    # Setup error logging
    errorLogger = logging.getLogger('error_logger')
    # Print Stderr to error logger with a timestamp
    for line in buf.rstrip().splitlines():
        errorLogger.error("{}  - {}".format(datetime.now(), line.rstrip()))


# Main Menu - Structure very similar to all other menus in program
def main():
    try:
        while True:
            option = input(
                "\nMain Menu: \nChoose a Option (based on the corresponding number):"
                "\n1. Logger Control & Config\n2. Download & Process Data \n3. General Settings \n4. About \n5. Quit" 
                "\n\nOption Chosen: ")
            # Set Menu Names
            if option == "1":
                logCtrl.init()
            elif option == "2":
                processData.init()
            elif option == "3":
                generalSettings.init()
            elif option == "4":
                about.init()
            elif option == "5":
                common.quit()
            else:
                common.other()
    # Used to break the loop if someone selects a back option.
    # No back option as this is root menu: this is left here for sake of consistency with other menus.
    except StopIteration:
        pass
