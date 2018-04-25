# This is the main Raspberry Pi Logging Script
# It has 3 sections: 1. Import, 2. Print Settings, 3. Log These are called at the bottom of the program
# 1. Calls the init() function which loads config by calling generalImport() and are lettingsImport().
# General settings (dictionary) and input specific settings (as objects) creating a list of pins to log
# 2. Iterates through lists and nicely formats and prints data
# 3. Setup logging (time interval etc.) then iterate through devices, grab data and save to CSV until stopped.

# Import Packages/Modules
import time
from datetime import datetime
from collections import OrderedDict
import configparser
import functools
import Adafruit_ADS1x15
import csv


class ADC:
    def __init__(self, section):
        self.name = section
        self.enabled = config[section].getboolean('enabled')
        self.inputType = config[section]['inputtype']
        self.gain = config[section].getint('gain')
        self.scaleLow = config[section].getint('scalelow')
        self.scaleHigh = config[section].getint('scalehigh')
        self.unit = config[section]['unit']

    # Go Through list of individual input objects and add those which are enabled to the 'master list'.
    # Then add their names to the header.
    def inputSetup(self):
        if self.enabled is True:
            adcToLog.append(adcPinMap[self.name])
            adcHeader.append(self.name)
        else:
            pass


# Initial Import and Setup
def init():
    # Setting up key variables for logging
    global dataRate
    dataRate = 860
    # List of pins to be logged and the list containing the logging functions
    global adcToLog
    adcToLog = []
    global adcHeader
    adcHeader = []
    # Dictionary used for creating ADC() objects
    global adcDict
    adcDict = OrderedDict()
    # A/D Setup - Create 4 Global instances of ADS1115 ADC (16-bit) according to Adafruit Libraries
    global adc0
    global adc1
    global adc2
    global adc3
    adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
    adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
    adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)

    # Open the config file
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')

    # Run Code to import general information
    generalImport()
    # Run code to import input settings
    inputImport()


# Import General Settings
def generalImport():
    print("Configuring General Settings")
    # Create dictionary for each item in the general section of the config
    global generalSettings
    generalSettings = OrderedDict()
    for key in config['General']:
        generalSettings[key] = config['General'][key]


# Import Input Settings
def inputImport():
    print("Configuring Input Settings")
    # For all sections but general, parse the data from config.C
    # Create a new object for each one. The init method of the class then imports all the data as instance variables
    for section in config.sections():
        if section != 'General':
            adcDict[section] = ADC(section)
    # ADC Pin Map List - created now the gain information has been grabbed.
    # This gives the list of possible functions that can be run to grab data from a pin.
    global adcPinMap
    adcPinMap = {
        "0A0": functools.partial(adc0.read_adc, 0, gain=adcDict["0A0"].gain, data_rate=dataRate),
        "0A1": functools.partial(adc0.read_adc, 1, gain=adcDict["0A1"].gain, data_rate=dataRate),
        "0A2": functools.partial(adc0.read_adc, 2, gain=adcDict["0A2"].gain, data_rate=dataRate),
        "0A3": functools.partial(adc0.read_adc, 3, gain=adcDict["0A3"].gain, data_rate=dataRate),
        "1A0": functools.partial(adc1.read_adc, 0, gain=adcDict["1A0"].gain, data_rate=dataRate),
        "1A1": functools.partial(adc1.read_adc, 1, gain=adcDict["1A1"].gain, data_rate=dataRate),
        "1A2": functools.partial(adc1.read_adc, 2, gain=adcDict["1A2"].gain, data_rate=dataRate),
        "1A3": functools.partial(adc1.read_adc, 3, gain=adcDict["1A3"].gain, data_rate=dataRate),
        "2A0": functools.partial(adc2.read_adc, 0, gain=adcDict["2A0"].gain, data_rate=dataRate),
        "2A1": functools.partial(adc2.read_adc, 1, gain=adcDict["2A1"].gain, data_rate=dataRate),
        "2A2": functools.partial(adc2.read_adc, 2, gain=adcDict["2A2"].gain, data_rate=dataRate),
        "2A3": functools.partial(adc2.read_adc, 3, gain=adcDict["2A3"].gain, data_rate=dataRate),
        "3A0": functools.partial(adc3.read_adc, 0, gain=adcDict["3A0"].gain, data_rate=dataRate),
        "3A1": functools.partial(adc3.read_adc, 1, gain=adcDict["3A1"].gain, data_rate=dataRate),
        "3A2": functools.partial(adc3.read_adc, 2, gain=adcDict["3A2"].gain, data_rate=dataRate),
        "3A3": functools.partial(adc3.read_adc, 3, gain=adcDict["3A3"].gain, data_rate=dataRate)
    }
    # Run code to choose which pins to be logged.
    for adc in adcDict:
        adcDict[adc].inputSetup()


# Output Current Settings
def settingsOutput():
    print("\nCurrent General Settings:")
    for key in generalSettings:
        print("{}: {}".format(key.title(), generalSettings[key]))
    print("\nCurrent Input Settings:")
    x = 0
    print(
        "|{:>6}|{:>6}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|".format("Number", "Name", "Pin Enabled", "Input Type", "Gain",
                                                                  "Scale", "Unit"))
    print("-" * 80)
    for ADC in adcDict:
        x += 1
        print("|{:>6}|{:>6}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x, adcDict[ADC].name, adcDict[ADC].enabled,
                                                                            adcDict[ADC].inputType, adcDict[ADC].gain,
                                                                            adcDict[ADC].scaleLow,
                                                                            adcDict[ADC].scaleHigh, adcDict[ADC].unit))


# Logging Script
def log():
    try:
        # Set Time Interval
        timeInterval = float(generalSettings['timeinterval'])
        # Find the length of what each row will be in the CSV (from which A/D are being logged)
        csvRows = len(adcToLog)
        # Set up list to be printed to CSV
        adcValues = [0] * csvRows
        # CSV - open file and add data on bottom
        with open('raw.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['(ID = generalSettings['uniqueid']'+'Date/Time', 'Time Interval (Seconds)'] + adcHeader)
            print("\nStart Logging...\n")

            # Set startTime (method used ignores changes in system clock time)
            startTime = time.perf_counter()

            # Beginning of reading script
            while (True):
                # Get time and send to Log
                currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f");
                timeElapsed = round(time.perf_counter() - startTime, 4)

                for currentPin, value in enumerate(adcToLog):
                    # Get Raw data from A/D, and add to adcValues list corresponding to the current pin
                    adcValues[currentPin] = (value())

                # Export Data to Spreadsheet inc current datetime and time elapsed and Reset list values (so we can see if code fails)
                writer.writerow([currentDateTime] + [timeElapsed] + adcValues)
                adcValues = [0] * csvRows
                # Work out time delay needed until next set of values taken based on user given value (using some clever maths)
                timeDiff = (time.perf_counter() - startTime)
                time.sleep(timeInterval - (timeDiff % timeInterval))

    except KeyboardInterrupt:
        print("Logging Finished")


# This is the code that is run when the program is loaded.
# If the module were to be imported, the code inside the if statement would not run.
# Calls the init() function and then the log() function
if __name__ == "__main__":
    # Load Config Data and Setup
    init()
    # Print Settings
    settingsOutput()
    # Run Logging
    log()
