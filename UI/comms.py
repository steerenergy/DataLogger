# Run from menu/py to select which hostname (i.e. which logger) the UI should upload/download data to/from
# Ensures this info can be accessed from the download and upload modules via the global variable 'loggerHostName'

import common
import ctypes
import configparser


class Host:
    # Run when an instance of the class 'Host' is created
    def __init__(self, welcomeMessage):
        self.host = None
        self.welcomeMessage = welcomeMessage
        # Import program config
        progConf = configparser.ConfigParser()
        progConf.optionxform = str
        progConf.read('progConf.ini')
        # Import hostnames from config
        self.hostnamesList = progConf['hostnames']
        # Run Hostname Selection
        self.hostnameSelect()

    def hostnameSelect(self):
        # Print Title
        print("Logger Hostnames Available (set in progConf.ini):")
        # Print Hostnames in dict
        for no in self.hostnamesList:
            print("{}. {}".format(no, self.hostnamesList[no]))

        # Hostname Selection
        while self.host is None:
            option = input("\nSelect the Hostname (by its corresponding number) of the Logger you wish to Use: ")
            try:
                # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
                if 0 < int(option) <= len(self.hostnamesList):
                    self.host = self.hostnamesList[option]
                    print("Success! - Hostname Set to: '{}' - To change hostname, restart this program".format(self.host))
                    # Update window title with the hostname
                    ctypes.windll.kernel32.SetConsoleTitleW("{} - {}".format(self.welcomeMessage, self.host))
                # When Integer is out of Range
                else:
                    common.other()
            # If someone does not put in an integer
            except ValueError:
                common.other()


# Allows for the hostname to be accessed across all modules
global loggerHostname
loggerHostname = None


# Create instance of class Host - this runs the __init__ as above
def init(welcomeMessage):
    global loggerHostname
    loggerHostname = Host(welcomeMessage)