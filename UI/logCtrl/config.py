# This program is a beast...
# It is in charge of creating and writing a config
# It begins at init(), on first time run offering to create a new config or import a previous.
# Menu is then initialised, user can change general settings (generalMenu()) or input (inputSetup())
# Once a user is happy, they enter saveUploadMenu() to write the config file and send via FTP over to the pi
# The save function also triggers preProcess().
# This generates m and c values (in y = mx + c) and saves to the config allowing for future processing


# Makes all directory references up a level to simplify importing common files
import configparser
import uuid
import paramiko
from . import common

# Flag for whether config has been set already
configSet = False


# Setting up the Class for the input setup
class ADC:
    # Create instance variables and set to default values (if prev config is not imported)
    def __init__(self):
        self.enabled = False
        self.inputType = "Edit Me"
        self.gain = 1
        self.scaleLow = 0
        self.scaleHigh = 0
        self.unit = "Edit Me 2"

    def enabledEdit(self):
        # If enabled, give option to disable, if disabled give option to enable
        if self.enabled is False:
            option = input("\nEnable Pin? (Y/N) ")
            if option == "Y" or option == "y":
                self.enabled = True
            elif option == "N" or option == "n":
                self.enabled = False
            else:
                common.other()
        elif self.enabled is True:
            option = input("\nDisable Pin? (Y/N) ")
            if option == "Y" or option == "y":
                self.enabled = False
            elif option == "N" or option == "n":
                self.enabled = True
            else:
                common.other()
        print("Success!\n")

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
        # Gain Settings will not change so it has been written like this.
        #  Users are instructed to type a number which corresponds to the value of gain they want
        gainSettings = ["1", "2", "4", "8", "16"]
        print("\nAvailable Gain Settings:")
        print("1 = +/-4.096V \n2 = +/-2.048V \n4 = +/-1.024V \n8 = +/-0.512V \n16 = +/-0.256V")
        option = input("\nPlease type in the gain setting you want: ")
        try:
            # check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if option in gainSettings:
                self.gain = option
                print("Success!")
            else:
                common.other()
        # If someone does not put in an integer
        except ValueError:
            common.other()

    def scaleEdit(self):
        option = input("\nWhat is the Low end of the Scale? ")
        self.scaleLow = option
        option = input("What is the High end of the Scale? ")
        self.scaleHigh = option

    def unitEdit(self):
        # List of Unit Types (this can be updated and the code will continue to work)
        print("\nAvailable Unit Types:")
        for pos, value in enumerate(unitTypes, start=1):
            print("{}. {}".format(pos, value))
        # Print one more option using list length for custom input
        print("{}\n{}. Custom Input".format("-"*15, len(unitTypes)+1))
        option = input("\nSelect an option by its corresponding number: ")
        try:
            # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if 0 < int(option) <= len(unitTypes):
                self.unit = unitTypes[int(option) - 1]
                print("Success!")
            elif int(option) == len(unitTypes)+1:
                self.unit = input("Please type in the unit you want to use"
                                  "\n(Note: If you want to add your unit to the default list, "
                                  "please edit 'progConf.ini')"
                                  "\n Unit:  ")
                print("Success!")
            # When Integer is out of Range
            else:
                common.other()
        # If someone does not put in an integer
        except ValueError:
            common.other()


# START HERE
def init():
    # If user has already entered config section, continue where they left off.
    # Otherwise, give option to create blank config file or to import previous logConf.ini file
    global configSet
    if configSet is False:
        progConfImport()
        option = input("\nDo you wish to load in your previous config (logConf.ini)? (Y/N) ")
        if option == "Y" or option == "y":
            configSet = True
            importConfInit()
        elif option == "N" or option == "n":
            configSet = True
            blankConfInit()
        else:
            common.other()

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
    # Initial Functions - setting up dictionaries with default values (will read config in future)
    # Setup dictionary with default settings for general settings
    global generalSettings
    generalSettings = {"timeinterval": 1, "name": "Default"}
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


# Init of input settings from logConf.ini file if user chooses
def importConfInit():
    try:
        # Get data from local logConf.ini file and import (code similar to the logger.py config code)
        global adcDict
        adcDict = {}
        # Open the config file
        logConf = configparser.ConfigParser()
        logConf.read('files/outbox/logConf.ini')

        # Create dictionary for each item in the general section of the logConf.ini
        global generalSettings
        generalSettings = {}
        for key in logConf['General']:
            if key != "uniqueid":
                generalSettings[key] = logConf['General'][key]

        # For all sections but general:
        # Parse the data from logConf and create a new object for each one and set instance variables for each
        for input in logConf.sections():
            if input != 'General':
                adcDict[input] = ADC()
                adcDict[input].enabled = logConf[input].getboolean('enabled')
                adcDict[input].inputType = logConf[input]['inputtype']
                adcDict[input].gain = logConf[input].getint('gain')
                adcDict[input].scaleLow = logConf[input].getint('scalelow')
                adcDict[input].scaleHigh = logConf[input].getint('scalehigh')
                adcDict[input].unit = logConf[input]['unit']
    except KeyError:
        print("Error Reading Config - Check logConf.ini exists in the same directory as this program")


# MAIN MENU
def menu():
    try:
        while True:
            option = input(
                "\nLogger Config Menu:  \nChoose a Option (based on the correspnding number): "
                "\n1. General Settings\n2. Input Setup\n3. Save/Upload Config\n4. Back"
                "\n\nOption Chosen: ")
            # Set Menu Names
            if option == "1":
                generalMenu()
            elif option == "2":
                inputSetup()
            elif option == "3":
                saveUploadMenu()
            elif option == "4":
                common.back()
            else:
                common.other()
    except StopIteration:
        pass


# GENERAL SETTINGS
def generalMenu():
    try:
        while True:
            print("\nConfig: General Settings: \nChoose a Option to edit a Setting (based on the correspnding number)")
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
    print("\nCurrent Time Interval is: {} Seconds\n".format(generalSettings["timeinterval"]))
    generalSettings["timeinterval"] = input("Enter New Time Interval: ")
    print("Success!\n")


# Name Setting
def generalName():
    print("\nCurrent Name is: {}\n".format(generalSettings["name"]))
    generalSettings["name"] = input("Enter New Name: ")
    print("Success!\n")


# INPUT SETUP
def inputSetup():
    inputCurrentSettings()
    chosenPin = input("\nPlease type the Name of Pin (Not the Number) you wish to Edit: ")
    if chosenPin in adcDict:
        # Main Menu
        try:
            while True:
                print(
                    "\nCurrent Pin Settings for: {}"
                    "\nChoose a Option to edit a Setting (based on the correspondingtre number)"
                    "\n1. Pin Enabled: {}\n2. Input Type: {}\n3. Gain: {}\n4. Scale: {} - {}\n5. Unit: {}"
                    "\n----------------\n6. Back".format(
                        chosenPin, adcDict[chosenPin].enabled, adcDict[chosenPin].inputType, adcDict[chosenPin].gain,
                        adcDict[chosenPin].scaleLow, adcDict[chosenPin].scaleHigh, adcDict[chosenPin].unit))
                option = input("\nOption Chosen: ")
                if option == "1":
                    adcDict[chosenPin].enabledEdit()
                elif option == "2":
                    adcDict[chosenPin].inputTypeEdit()
                elif option == "3":
                    adcDict[chosenPin].gainEdit()
                elif option == "4":
                    adcDict[chosenPin].scaleEdit()
                elif option == "5":
                    adcDict[chosenPin].unitEdit()
                elif option == "6":
                    common.back()
                else:
                    common.other()
        except StopIteration:
            pass
    else:
        common.other()
    # Bring up Options for editing
    # Next object


# Printing Current Input Settings
def inputCurrentSettings():
    print("Current Input Settings:\n")
    print("-" * 92)
    print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|".format("Number", "Name", "Pin Enabled", "Input Type",
                                                                      "Gain", "Scale", "Unit"))
    print("-" * 92)
    x = 0
    for ADC in adcDict:
        x += 1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x, ADC, adcDict[ADC].enabled,
                                                                              adcDict[ADC].inputType, adcDict[ADC].gain,
                                                                              adcDict[ADC].scaleLow,
                                                                              adcDict[ADC].scaleHigh,
                                                                              adcDict[ADC].unit))


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


# SAVE/UPLOAD
def saveUploadMenu():
    try:
        while True:
            print(
                "\nSave/Upload:\nChoose a Option (based on the corresponding number)"
                "\n1. Save \n2. Save and Upload\n3. Back")
            option = input("\nOption Chosen: ")
            if option == "1":
                save()
            elif option == "2":
                save()
                upload()
            elif option == "3":
                common.back()
            else:
                common.other()
    except StopIteration:
        pass


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

    # Write data for each A/D
    for key in adcDict:
        logConf[key] = {}
        logConf[key]["enabled"] = str(adcDict[key].enabled)
        logConf[key]["inputtype"] = str(adcDict[key].inputType)
        logConf[key]["gain"] = str(adcDict[key].gain)
        logConf[key]["scalelow"] = str(adcDict[key].scaleLow)
        logConf[key]["scalehigh"] = str(adcDict[key].scaleHigh)
        logConf[key]["unit"] = str(adcDict[key].unit)
        # Only calculate scales if pin enabled
        if adcDict[key].enabled is True:
            # This is where m and c are calculated
            # Note that the lowScale, highScale, input type and gain are all still written to the config
            m, c = preProcess(adcDict[key].scaleLow, adcDict[key].scaleHigh, adcDict[key].inputType, adcDict[key].gain)
            logConf[key]["m"] = str(m)
            logConf[key]["c"] = str(c)
    # Write File
    with open('files/outbox/logConf.ini', 'w') as configfile:
        logConf.write(configfile)
    print("Success!")
    print("NOTE - If you manually change the logConf.ini file contents, you must rerun this program,"
          "load in the config file and save it. Otherwise, the data will be processed incorrectly. ")


# FTP Upload of Config File
def upload():
    try:
        print("\nPreparing to Transfer...")
        # Open a transport
        host = "raspberrypi"
        port = 22
        transport = paramiko.Transport((host, port))
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
        print("Success!")
    finally:
        sftp.close()
        transport.close()


# Temp Code
if __name__ == "__main__":
    init()
