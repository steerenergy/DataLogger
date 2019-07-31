# This is the main Raspberry Pi Logging Script
# It has 3 sections: 1. Import, 2. Print Settings, 3. Log These are called at the bottom of the program
# 1. Calls the init() function which loads config by calling generalImport() and are lettingsImport().
# General settings (dictionary) and input specific settings (as objects) creating a list of pins to log
# 2. Iterates through lists and nicely formats and prints data
# 3. Setup logging (time interval etc.) then iterate through devices, grab data and save to CSV until stopped.

# Import Packages/Modules
import time
from datetime import datetime, timedelta
from collections import OrderedDict
import configparser
import functools
# Uncomment below for real adc (if running on Pi)
import Adafruit_ADS1x15
# Uncomment below for fake adc simulation if using a PC
# import Adafruit_ADS1x15Fake as Adafruit_ADS1x15
import csv
import threading
import shutil
import os

# Contains information about each pin
class ADC:
    def __init__(self, section):
        self.name = section
        self.enabled = config[section].getboolean('enabled')
        self.friendlyName = config[section]['friendlyName']
        self.inputType = config[section]['inputtype']
        self.gain = config[section].getint('gain')
        self.scaleLow = config[section].getfloat('scalelow')
        self.scaleHigh = config[section].getfloat('scalehigh')
        self.unit = config[section]['unit']
        if "m" in config[section] and "c" in config[section]:
            self.m = config[section].getfloat('m')
            self.c = config[section].getfloat('c')

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
    # Flag for multithreaded (GUI) use to be triggered to stop logging loop
    global logEnbl
    logEnbl = True
    # dataRate of the A/D (see the ADS1115 datasheet for more info)
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
    # Where Complete list of ADC values is stored after all pins logged
    global adcValuesCompl
    adcValuesCompl = []
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
    config.read('files/inbox/logConf.ini')

    # Run Code to import general information
    generalImport()
    # Run code to import input settings
    inputImport()


# Import General Settings
def generalImport():
    print("Configuring General Settings... ", end="", flush=True)
    # Create dictionary for each item in the general section of the config
    global generalSettings
    generalSettings = OrderedDict()
    try:
        for key in config['General']:
            generalSettings[key] = config['General'][key]
        print("Success!")
    # Exception raised when key cannot be found (file doesnt't exist or file is corrupt)
    except KeyError:
        print("ERROR - Failed to read General Settings - Have you sent over a 'logConf.ini' file?")
        global logEnbl
        logEnbl = False


# Import Input Settings
def inputImport():
    print("Configuring Input Settings... ", end="", flush=True)
    # For all sections but general, parse the data from config.C
    # Create a new object for each one. The init method of the class then imports all the data as instance variables
    try:
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
        print("Success!")

    # Exception raised when key cannot be found (file doesnt't exist or file is corrupt)
    except KeyError:
        print("ERROR - Failed to read Input Settings - Have you sent over a 'logConf.ini' file?")
        global logEnbl
        logEnbl = False


# Output Current Settings
def settingsOutput():
    # Print General Settings then Input Settings
    print("\nCurrent General Settings:")
    for key in generalSettings:
        print("{}: {}".format(key.title(), generalSettings[key]))
    print("\nCurrent Input Settings: (Settings hidden for Disabled Inputs)")
    x = 0
    print("-" * 65)
    # Top Row Headings
    print(
        "|{:>2}|{:>4}|{:>5}|{:>10}|{:>10}|{:>4}|{:>12}|{:>9}|".format("No", "Name", "Enbl", "F.Name", "Input Type",
                                                                      "Gain", "Scale", "Unit"))
    print("-" * 65)
    # Print input settings for each Pin
    for pin in adcDict:
        # Only print full settings if that channel is enabled
        x += 1
        if adcDict[pin].enabled == 1:
            print("|{:>2}|{:>4}|{:>5}|{:>10}|{:>10}|{:>4}|{:>6}{:>6}|{:>9}|".format(x, adcDict[pin].name,
                                                                                    str(adcDict[pin].enabled),
                                                                                    adcDict[pin].friendlyName,
                                                                                    adcDict[pin].inputType,
                                                                                    adcDict[pin].gain,
                                                                                    adcDict[pin].scaleLow,
                                                                                    adcDict[pin].scaleHigh,
                                                                                    adcDict[pin].unit))
        # If channel not enabled
        else:
            print("|{:>2}|{:>4}|{:>5}|{:>10}|{:>10}|{:>4}|{:>6}{:>6}|{:>9}|".format(x, adcDict[pin].name,
                                                                                    str(adcDict[pin].enabled),
                                                                                    "-",
                                                                                    "-",
                                                                                    "-",
                                                                                    "-",
                                                                                    "-",
                                                                                    "-"))
# Logging Script
def log():
    # Set Time Interval
    timeInterval = float(generalSettings['timeinterval'])
    # Find the length of what each row will be in the CSV (from which A/D are being logged)
    csvRows = len(adcToLog)
    # Set up list to be printed to CSV
    adcValues = [0] * csvRows
    # Get timestamp for filename
    timeStamp = datetime.now().strftime("%Y%m%d-%H%M%S.%f")

    # FILE MANAGEMENT
    print("\nDisk Usage:")
    # Get Users Remaining Disk Space - (Convert it from Bytes into MegaBytes)
    remainingSpace = (shutil.disk_usage(os.path.realpath('/'))[2] / 1e6)
    # Output space - rounding to a nice number
    print("Current Free Disk Space: {} MB".format(round(remainingSpace, 2)))

    # Calculate amount of time left for logging
    # Find out Size (in MB) of Each Row
    rowMBytes = 7 / 1e6
    # Find amount of MB written each second
    MBEachSecond = (rowMBytes * csvRows) / timeInterval
    # Calculate time remaining using free space
    timeRemSeconds = remainingSpace / MBEachSecond
    # Add time in seconds to current datetime to give data it will run out of space
    timeRemDate = datetime.now() + timedelta(0, timeRemSeconds)
    print("With the current config, you will run out of space on approximately: {}"
          "\nIf you need more space, use the UI to download previous logs and delete them on the Pi."
          .format(timeRemDate.strftime("%Y-%m-%d %H:%M:%S")))

    # Make copy of logConf.ini with new name that includes timestamp
    shutil.copyfile('files/inbox/logConf.ini', 'files/outbox/logConf{}.ini'.format(timeStamp))

    # CSV - Create/Open CSV file and print headers
    with open('files/outbox/raw{}.csv'.format(timeStamp), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date/Time', 'Time Interval (seconds)'] + adcHeader)
        print("\nStart Logging...\n")

        # Start live data thread
        dataThread = threading.Thread(target=liveData)
        dataThread.start()

        # Set startTime (method used ignores changes in system clock time)
        startTime = time.perf_counter()

        # Beginning of reading script
        while logEnbl is True:
            # Get time and send to Log
            currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            timeElapsed = round(time.perf_counter() - startTime, 2)

            for currentPin, value in enumerate(adcToLog):
                # Get Raw data from A/D, and add to adcValues list corresponding to the current pin
                adcValues[currentPin] = (value())

            # Export Data to Spreadsheet inc current datetime and time elapsed
            writer.writerow([currentDateTime] + [timeElapsed] + adcValues)
            # Copy list for data output and reset list values (so we can see if code fails)
            global adcValuesCompl
            adcValuesCompl = adcValues
            adcValues = [0] * csvRows
            # Work out time delay needed until next set of values taken based on user given value
            # (Using some clever maths)
            timeDiff = (time.perf_counter() - startTime)
            time.sleep(timeInterval - (timeDiff % timeInterval))
        # Wait until live data thread is finished
        dataThread.join()


# Live Data Output
# Function is run in separate thread to ensure it doesn't interfere with logging
def liveData():
    # Setup data buffer to hold most recent data
    print("Live Data:\n")
    # Print header for all pins being logged
    adcHeaderPrint = ""
    for pinName in adcHeader:
        adcHeaderPrint += ("|{:>3}{:>5}".format(pinName, adcDict[pinName].unit))
    print("{}|".format(adcHeaderPrint))
    # Print a nice vertical line so it all looks pretty
    print("-" * (9 * len(adcHeader) + 1))
    buffer = 0
    # Don't print live data when adcValuesCompl doesn't exist. Also if logging is stopped, exit loop
    while not adcValuesCompl and logEnbl is True:
        pass
    # Livedata Loop - Loops Forever until LogEnbl is False (controlled by GUI)
    while logEnbl is True:
        # Get Complete Set of Logged Data
        # If Data is different to that in the buffer
        if adcValuesCompl != buffer:
            buffer = adcValuesCompl
            adcValuesComplPrint = ""
            # Create a nice string to print with the values in
            # Only prints data that is being logged
            for no, val in enumerate(adcValuesCompl):
                # Get the name of the pin so it can be used to find the adc object
                pinName = adcHeader[no]
                # Calculate converted value
                convertedVal = val * adcDict[pinName].m + adcDict[pinName].c
                # Add converted value to the string being printed
                adcValuesComplPrint += ("|{:>8}".format(round(convertedVal, 2)))
            print("{}|".format(adcValuesComplPrint))
        # Sleep - Don't want to go too fast
        time.sleep(0.05)


# Contains functions for normal run of logger
def run():
    # Load Config Data and Setup
    init()
    # Only continue if import was successful
    if logEnbl is True:
        # Print Settings
        settingsOutput()
        # Run Logging
        log()


# This is the code that is run when the program is loaded.
# If the module were to be imported, the code inside the if statement would not run.
# Calls the init() function and then the log() function
if __name__ == "__main__":
    # Warning about lack of CSV
    print("\nWARNING - running this script directly may produce a blank CSV. "
          "\nIf you need data to be recorded, use 'gui.py'\n")
    # Run logger as per normal setup
    run()
