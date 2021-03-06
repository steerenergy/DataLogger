# This program is a beast...
# It is in charge of creating and writing a config
# It begins at init(), on first time it imports the previously saved 'logConf.ini' under 'files/outbox' if it exists
# Menu is then initialised, user can change general settings (generalMenu()) or input (inputSetup())
# They can import a different config file from 'files/storedConfigs' if they wish using configFileSelect()
# Once the user is happy, they can save (save()) the file or save and upload (save() followed by upload())
# The save function also triggers preProcess()- generating m and c values (in y = mx + c)
# These are saved to the config, and are used by the logger and process() to convert data laterto true values later

# Makes all directory references up a level to simplify importing common files
import configparser
import uuid
import paramiko
import common
import comms
import os
import socket

# Flag for whether config has been set already
configSet = False


# Class holding all the inputs
class ADC:
    # Create instance variables and set to default values (if prev config is not imported)
    def __init__(self):
        self.enabled = False
        self.friendlyName = "Edit Me"
        self.inputType = "Edit Me"
        self.gain = 1
        self.scaleLow = 0
        self.scaleHigh = 0
        self.unit = "Edit Me"

    def enabledEdit(self):
        # Toggle Pin on and Off
        if self.enabled is False:
            self.enabled = True
            print("Pin Enabled")
        elif self.enabled is True:
            self.enabled = False
            print("Pin Disabled")

    def friendlyNameEdit(self):
        option = input("\nType in your chosen friendly name for the pin (max 10 characters) ")
        # If friendly name is within character limit, set it. Otherwise, show error
        if len(option) <= 10:
            self.friendlyName = option
        else:
            common.other()

    def inputTypeEdit(self):
        # List of input Types (this can be updated and the code will continue to work)
        print("\nAvailable Input Types:")
        for pos, value in enumerate(inputTypes, start=1):
            print("{}. {}".format(pos, value))
        option = input("\n(Note - To change available input types please edit 'progConf.ini'"
                       "\nSelect an option by its corresponding number: ")
        try:
            # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if 0 < int(option) <= len(inputTypes):
                self.inputType = inputTypes[int(option) - 1]
                print("Success!")
            else:
                common.other()
        # If someone does not put in an integer
        except ValueError:
            common.other()

    def gainEdit(self):
        # Values for Gain can be changed below although this should not need to happen
        # Users are instructed to type a number which corresponds to the value of gain they want
        gainSettings = [1, 2, 4, 8, 16]
        print("\nAvailable Gain Settings (See User Manual for More Info):")
        print("|Gain|Full Scale Voltage|")
        print("-" * 25)
        print("|1   |      4.096V      |\n|2   |      2.048V      |\n|4   "
              "|      1.024V      |\n|8   |      0.512V      |\n|16  |      0.256V      |")
        option = input("\nPlease type in the gain setting you want: ")
        try:
            # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if option in gainSettings:
                self.gain = option
                print("Success!")
            else:
                common.other()
        # If someone does not put in an integer
        except ValueError:
            common.other()

    def scaleEdit(self):
        # Set the high and low end of the scale
        try:
            option = float(input("\nWhat is the Low end of the Scale (Excluding Units)? "))
            self.scaleLow = option
            option = float(input("What is the High end of the Scale (Excluding Units)? "))
            self.scaleHigh = option
        except ValueError:
            common.other()

    def unitEdit(self):
        # List of Unit Types (from progConf.ini)
        print("\nAvailable Unit Types:")
        for pos, value in enumerate(unitTypes, start=1):
            print("{}. {}".format(pos, value))
        # Print one more option using list length for custom input
        print("{}\n{}. Custom Input".format("-" * 15, len(unitTypes) + 1))
        option = input("\nSelect an option by its corresponding number: ")
        try:
            # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if 0 < int(option) <= len(unitTypes):
                self.unit = unitTypes[int(option) - 1]
                print("Success!")
            elif int(option) == len(unitTypes) + 1:
                entry = input("\nPlease type in the unit you want to use (Max 7 Characters)"
                              "\n(Note: If you want to add your unit to the default list, "
                              "please edit 'progConf.ini')"
                              "\nUnit:  ")
                # If unit is within character limit, set it. Otherwise, show error
                if len(entry) <= 9:
                    self.unit = entry
                    print("Success!")
                else:
                    common.other()
            # When Integer is out of Range
            else:
                common.other()
        # If someone does not put in an integer
        except ValueError:
            common.other()


# PROGRAM STARTS HERE
def init():
    # If user has already entered config section, continue where they left off.
    # Otherwise, give option to create blank config file or to import previous logConf.ini file
    # 'configSet' variable flag used to ensure the config is only
    # imported/default config generated  the first time the program runs
    global configSet
    if configSet is False:
        progConfImport()
        # If 'logConf.ini' file found in the files/outbox then import this file, otherwise create default config
        if 'logConf.ini' in os.listdir('files/outbox/'):
            print("\nImporting Previously Saved Config File...")
            # Set flag to show config has now been set
            configSet = True
            # Send argument of location of logConf.ini to import file
            # Placing the function inside print will print a success message at the end
            print(importConfInit('files/outbox/logConf.ini'))

        # If Config File doesn't exist
        else:
            print("\nNo Config File Found - Creating Default Template...")
            # Set flag to show config has now been set
            configSet = True
            blankConfInit()

    # Load Menu
    menu()


# CONFIG IMPORTS - Program Config Import for input types and units + global vars for data pre processing
def progConfImport():
    # Create config object, make it preserve case on import and read config file
    progConf = configparser.ConfigParser()
    progConf.optionxform = str
    progConf.read('progConf.ini')

    # Create list of unitTypes from unitType section
    global unitTypes
    unitTypes = []
    for key in progConf['unitTypes']:
        unitTypes.append(progConf['unitTypes'][key])
    # Create list of inputTypes from the inputTypes section
    global inputTypes
    inputTypes = []
    for key in progConf['inputTypes']:
        inputTypes.append(key)

    # Lists and dicts or pre processing load in
    # Gain list used for conversion from raw to voltage
    global gainList
    gainList = {
        1: 4.096,
        2: 2.04,
        4: 1.024,
        8: 0.512,
        16: 0.256
    }
    # Creating a dictionary of input types from progConf file
    # It contains a tuple with the value (in volts) for the low and high end of the scale
    # Note: We got a list of input type names earlier but here we actually get the min and max values (the scale)
    # Changing the above code would involve lots of time restructuring which I don't have
    global inputTypeDict
    inputTypeDict = {}
    for key in progConf['inputTypes']:
        inputTypeDict[key] = eval(progConf['inputTypes'][key])


# Init of input settings if user chooses a blank config
def blankConfInit():
    # Setup dictionary with default settings for general settings
    global generalSettings
    generalSettings = {"timeinterval": 1.0, "name": "Default"}
    # Init all objects for 16 channels.
    global adcDict
    adcDict = {
        "0A0": ADC(),
        "0A1": ADC(),
        "0A2": ADC(),
        "0A3": ADC(),
        "1A0": ADC(),
        "1A1": ADC(),
        "1A2": ADC(),
        "1A3": ADC(),
        "2A0": ADC(),
        "2A1": ADC(),
        "2A2": ADC(),
        "2A3": ADC(),
        "3A0": ADC(),
        "3A1": ADC(),
        "3A2": ADC(),
        "3A3": ADC()
    }


# Init of logger settings from logConf.ini file
def importConfInit(configPath):
    # Get data from local logConf.ini file and import (code similar to the logger.py config code)
    global adcDict
    adcDict = {}
    # Open the config file
    logConf = configparser.ConfigParser()
    logConf.read(configPath)

    # Create dictionary for each item in the general section of the logConf.ini
    global generalSettings
    generalSettings = {}
    for key in logConf['General']:
        # Don't allow user to change uniqueId as this is automatically generated
        if key != "uniqueid":
            generalSettings[key] = logConf['General'][key]

    # For all sections but general:
    # Parse the data from logConf and create a new object for each one and set instance variables for each
    for pin in logConf.sections():
        if pin != 'General':
            adcDict[pin] = ADC()
            adcDict[pin].enabled = logConf[pin].getboolean('enabled')
            adcDict[pin].friendlyName = logConf[pin]['friendlyname']
            adcDict[pin].inputType = logConf[pin]['inputtype']
            adcDict[pin].gain = logConf[pin].getint('gain')
            adcDict[pin].scaleLow = logConf[pin].getfloat('scalelow')
            adcDict[pin].scaleHigh = logConf[pin].getfloat('scalehigh')
            adcDict[pin].unit = logConf[pin]['unit']
    return "Success! - '{}' Imported".format(configPath)


# MAIN MENU
def menu():
    try:
        while True:
            option = input(
                "\nLogger Config Menu:  \nChoose a Option (based on the corresponding number): "
                "\n1. General Settings\n2. Input Setup\n3. Save and Upload Config\n4. Save Config (Don't Upload)"
                "\n5. Import Stored Config\n6. Back\n\nOption Chosen: ")
            # Set Menu Names
            if option == "1":
                generalMenu()
            elif option == "2":
                inputSetup()
            elif option == "3":
                # Runs save function - and returns 'True' if the save failed for some reason
                # Used so it doesn't upload a file if the save was unsuccessful
                saveFailed = save()
                if saveFailed is True:
                    print("ERROR - Save Upload Failed")
                else:
                    upload()
            elif option == "4":
                save()
            elif option == "5":
                configImportSelect()
            elif option == "6":
                # Warn users that unsaved changes will be lost
                print("\nWARNING: Any unsaved changes will be lost on program close!\n")
                common.back()
            else:
                common.other()
    except StopIteration:
        pass


# GENERAL SETTINGS
def generalMenu():
    try:
        while True:
            print("\nConfig: General Settings: \nChoose a Option to edit a Setting (based on the corresponding number)")
            x = 0
            for key in generalSettings:
                x += 1
                print("{}. {}: {}".format(x, key.title(), generalSettings[key]))
            print("----------------\n{}. Back".format(x + 1))
            option = input("\nOption Chosen: ")
            if option == "1":
                generalTime()
            elif option == "2":
                generalName()
            elif option == "3":
                common.back()
            else:
                common.other()
    except StopIteration:
        pass


# Time Setting
def generalTime():
    # Print Current time Interval
    print("\nCurrent Time Interval is: {} second(s)\n".format(generalSettings["timeinterval"]))
    # Get user to input new time interval and check it's valid
    try:
        interval = float(input("Enter New Time Interval (min 0.1): "))
        # Only change time interval if a valid int above 0.1 seconds
        # (note this will not stop users editing the config for time intervals less than 0.1 seconds
        if interval >= 0.1:
            generalSettings["timeinterval"] = interval
            print("Success!\n")
        else:
            common.other()

        print("NOTE: Time intervals less than 0.1 seconds can be configured by manually editing logConf.ini "
              "before importing.\nThis is beyond the specification of the logger so do so at your own risk!")
    except ValueError:
        common.other()


# Name Setting
def generalName():
    print("\nCurrent Name is: {}\n".format(generalSettings["name"]))
    generalSettings["name"] = input("Enter New Name: ")
    print("Success!\n")


# INPUT SETUP
def inputSetup():
    try:
        # Stay in input selection until user leaves pressing 'Enter'
        while True:
            try:
                # Current Settings Print Out
                inputCurrentSettings()
                userInput = input("\nType the number corresponding to the pin you wish to Edit "
                                  "or press 'Enter' to go back: ")
                if str(userInput) == '':
                    print("Going Back")
                    common.back()
                # Find on adcDict if number is in adcDict, else throw an error
                # If Found in adcDict, set the device to adcDict and continue
                elif int(userInput) > 0 and int(userInput) - 1 < len(adcDict):
                    chosenNum = int(userInput)
                    chosenPin = list(adcDict.items())[chosenNum - 1][0]
                    # Input Selection Menu
                    try:
                        while True:
                            print(
                                "\nCurrent Pin Settings for: {}"
                                "\nChoose a Option to edit a Setting (based on the corresponding number)"
                                "\n1. Pin Enabled: {}\n2. Friendly Name: {}\n3. Input Type: {}\n4. Gain: {}\n"
                                "5. Scale: {} - {}\n6. Unit: {}"
                                "\n----------------\n7. Back".format(
                                    chosenPin, adcDict[chosenPin].enabled, adcDict[chosenPin].friendlyName,
                                    adcDict[chosenPin].inputType, adcDict[chosenPin].gain,
                                    adcDict[chosenPin].scaleLow, adcDict[chosenPin].scaleHigh, adcDict[chosenPin].unit))
                            option = input("\nOption Chosen: ")
                            if option == "1":
                                adcDict[chosenPin].enabledEdit()
                            elif option == "2":
                                adcDict[chosenPin].friendlyNameEdit()
                            elif option == "3":
                                adcDict[chosenPin].inputTypeEdit()
                            elif option == "4":
                                adcDict[chosenPin].gainEdit()
                            elif option == "5":
                                adcDict[chosenPin].scaleEdit()
                            elif option == "6":
                                adcDict[chosenPin].unitEdit()
                            elif option == "7":
                                common.back()
                            else:
                                common.other()
                    except StopIteration:
                        pass
                else:
                    common.other()
            # If someone doesn't type in an integer or press Enter
            except ValueError:
                common.other()
    # Used to break the loop if someone selects a back option.
    except StopIteration:
        pass


# Printing Current Input Settings
def inputCurrentSettings():
    print("\nCurrent Input Settings:")
    print("-" * 97)
    print("|{:>6}|{:>6}|{:>12}|{:>14}|{:>12}|{:>12}|{:>14}|{:>12}|".format("Number", "Name", "Pin Enabled",
                                                                           "Friendly Name", "Input Type", "Gain",
                                                                           "Scale", "Unit"))
    print("-" * 97)
    x = 0
    for pin in adcDict:
        x += 1
        if adcDict[pin].enabled == 1:
            print("|{:>6}|{:>6}|{:>12}|{:>14}|{:>12}|{:>12}|{:>7}{:>7}|{:>12}|".format(x,
                                                                                       pin,
                                                                                       str(adcDict[pin].enabled),
                                                                                       adcDict[pin].friendlyName,
                                                                                       adcDict[pin].inputType,
                                                                                       adcDict[pin].gain,
                                                                                       adcDict[pin].scaleLow,
                                                                                       adcDict[pin].scaleHigh,
                                                                                       adcDict[pin].unit))

        else:
            print("|{:>6}|{:>6}|{:>12}|{:>14}|{:>12}|{:>12}|{:>7}{:>7}|{:>12}|".format(x,
                                                                                       pin,
                                                                                       str(adcDict[pin].enabled),
                                                                                       "-",
                                                                                       "-",
                                                                                       "-",
                                                                                       "-",
                                                                                       "-",
                                                                                       "-"))


# PRE PROCESS - Called by Save Function to determine
# Generate 'm' and 'c' to be used in processing data
def preProcess(scaleLow, scaleHigh, inputType, gainVal):
    # Effectively using y = mx+c
    # Scale chosen on y axis, inputType on x axis (in Volts))
    inputLow = inputTypeDict[inputType][0]
    inputHigh = inputTypeDict[inputType][1]
    m = (scaleHigh - scaleLow) / (inputHigh - inputLow)
    c = scaleHigh - m * inputHigh
    # As data recorded is raw, and 'x' must be in volts, m is multiplied by the gain scale factor
    m = m * gainList[gainVal] / 32767.0
    return m, c


# Save Data to Config File
def save():
    # Config Setup
    print("\nSaving Config File...")
    logConf = configparser.ConfigParser()

    # Write Sections
    logConf["General"] = {}
    for key in generalSettings:
        logConf["General"][key] = str(generalSettings[key])
    logConf["General"]["uniqueid"] = str(uuid.uuid4())

    try:
        # Write data for each A/D
        for key in adcDict:
            logConf[key] = {}
            logConf[key]["enabled"] = str(adcDict[key].enabled)
            logConf[key]["friendlyname"] = str(adcDict[key].friendlyName)
            logConf[key]["inputtype"] = str(adcDict[key].inputType)
            logConf[key]["gain"] = str(adcDict[key].gain)
            logConf[key]["scalelow"] = str(adcDict[key].scaleLow)
            logConf[key]["scalehigh"] = str(adcDict[key].scaleHigh)
            logConf[key]["unit"] = str(adcDict[key].unit)
            # Only calculate scales if pin enabled
            if adcDict[key].enabled is True:
                # This is where m and c are calculated
                # Note that the lowScale, highScale, input type and gain are all still written to the config
                m, c = preProcess(adcDict[key].scaleLow, adcDict[key].scaleHigh,
                                  adcDict[key].inputType, adcDict[key].gain)
                logConf[key]["m"] = str(m)
                logConf[key]["c"] = str(c)
        # Write File
        directory = 'files/outbox/logConf.ini'
        with open(directory, 'w') as configfile:
            logConf.write(configfile)
        print("Success! - Config Saved To: '{}'".format(directory))
        print("NOTE - If you manually change the logConf.ini file contents, you must rerun this program, "
              "load in the config file and save it. Otherwise, the data will be processed incorrectly. ")
    except KeyError as e:
        print("ERROR - Unable to Write Config (Invalid Config Entry - {})"
              " - Have you set your input name and scale to a valid setting?".format(str(e)))
        return True


# FTP Upload of Config File
def upload():
    try:
        print("\nPreparing to Transfer To: '{}'...".format(comms.loggerHostname.host))
        # Open a transport + import hostname
        port = 22
        transport = paramiko.Transport(comms.loggerHostname.host, port)
        # Auth
        password = "raspberry"
        username = "pi"
        transport.connect(username=username, password=password)
        # Go!
        print("Transferring Config...")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
        remotePath = '/home/pi/Github/DataLogger/RPI/files/inbox/logConf.ini'
        localPath = 'files/outbox/logConf.ini'
        sftp.put(localPath, remotePath)
        # Close Connection
        sftp.close()
        transport.close()
        # Print Success
        print("Success! - Configuration File Successfully Transferred"
              "\nYou may now start the logger using the touchscreen")
        # Close Connection
        sftp.close()
        transport.close()

    # If connection was unsuccessful
    except (socket.error, paramiko.SSHException) as e:
        print("ERROR: Failed To Trasnfer Config To: '{}' - "
              "Ensure you are Connected to the same Network as the Logger and Try Again"
              .format(comms.loggerHostname.host))
        # Print Error Info
        print(e)
        # Close Connection if possible
        try:
            sftp.close()
            transport.close()
        # If the above variables haven't been assigned yet, move on
        except UnboundLocalError:
            pass


# Allows user to import any file in 'files/storedConfigs' if they wish
def configImportSelect():
    # Set Directory of config files
    directory = 'files/storedConfigs/'
    # Create list of all files in directory
    directoryFiles = os.listdir(directory)
    configList = [fileName for fileName in directoryFiles if fileName.endswith('.ini')]

    # Dealing with cases where there are no matching files in directory
    if len(configList) <= 0:
        print("\nNo Config Files found - "
              "Please ensure there is at least 1 file ending in '.ini' in '{}'".format(directory))
    else:
        try:
            # List config files found
            print("\nFiles ending in '.ini' found in '{}':".format(directory))
            # Print Output in nice format
            for pos, fileName in enumerate(configList, start=1):
                print("{}. {}".format(pos, fileName))

            # User file selection
            configFile = int(input("Please select a file (by its corresponding number):  "))
            # If number valid on list, choose that config file
            if 0 < configFile <= len(configList):
                # Warn users of risk of importing a new file
                option = input("\nWARNING: Importing a new config will erase currently imported Settings!"
                               " - Make sure you save your current configuration before importing new settings"
                               "\nDo You Wish to Continue? (Y/N): ")
                if option == "Y" or option == "y":
                    # Call function to import config at new directory
                    # Placing the function inside print will print a success message at the end
                    print(importConfInit(directory + fileName))
                elif option == "N" or option == "n":
                    print("Import Cancelled")
                else:
                    print("Invalid Option: Import Cancelled")

            # If a number is typed in out of range
            else:
                common.other()
        # If a user doesn't type in an integer
        except ValueError:
            common.other()


