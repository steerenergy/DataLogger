#Makes all directory references up a level to simplify importing common files
import sys
import configparser
import uuid
import paramiko
sys.path.append("..")
import common
configSet = False

#Setting up the Class for the input setup
class ADC:
    def __init__(self):
        self.enabled = False
        self.inputType = "Edit Me"
        self.gain = 1
        self.scaleLow = 0
        self.scaleHigh = 0
        self.unit = "Edit Me 2"

    def enabledEdit(self):
    #If enabled, give option to disable, if disabled give option to enable
            if self.enabled == False:
                option = input("\nEnable Pin? (Y/N) ")
                if option == "Y" or option == "y":
                    self.enabled = True
                elif option == "N" or option == "n":
                    self.enabled = False
                else:
                    common.other()
            elif self.enabled == True:
                option = input("\nDisable Pin? (Y/N) ")
                if option == "Y" or option == "y":
                    self.enabled = False
                elif option == "N" or option == "n":
                    self.enabled = True
                else:
                    common.other()
            print("Success\n")

    def inputTypeEdit(self):
        #List of input Types (this can be updated and the code will continue to work)
        inputTypes = ["4-20mA","0-2V","0-10V"]
        print("\nAvaiable Input Types:")
        for key, value in enumerate(inputTypes,start=1):
            print("{}. {}".format(key,value))
        option = input("\nSelect an option by its corresponding number: ")
        try:
            #check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if 0<int(option)<=len(inputTypes):
                self.inputType = inputTypes[int(option)-1]
                print("Success")
            else:
                common.other()
        #If someone does not put in an integer
        except ValueError:
                common.other()

    def gainEdit(self):
                #Gain Settigns will not change so it has been written like this. Users are instructed to type a number which corresponds to the value of gain they want
                gainSettings = ["1","2","4","8","16"]
                print("\nAvaiable Gain Settings:")
                print("1 = +/-4.096V \n2 = +/-2.048V \n4 = +/-1.024V \n8 = +/-0.512V \n16 = +/-0.256V")
                option = input("\nPlease type in the gain setting you want: ")
                try:
                    #check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
                    if option in gainSettings:
                        self.gain = option
                        print("Success")
                    else:
                        common.other()
                #If someone does not put in an integer
                except ValueError:
                        common.other()
    def scaleEdit(self):
        option = input("\nWhat is the Low end of the Scale? ")
        self.scaleLow = option
        option = input("What is the High end of the Scale? ")
        self.scaleHigh = option

    def unitEdit(self):
        #List of Unit Types (this can be updated and the code will continue to work)
        unitTypes = ["N","m","mBar","mm","V","mV","A"]
        print("\nAvaiable Unit Types:")
        for key, value in enumerate(unitTypes,start=1):
            print("{}. {}".format(key,value))
        option = input("\nSelect an option by its corresponding number: ")
        try:
            #check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
            if 0<int(option)<=len(unitTypes):
                self.unit= unitTypes[int(option)-1]
                print("Success")
            else:
                common.other()
        #If someone does not put in an integer
        except ValueError:
                common.other()

def init():
    #Determine whether a config inside the program has already been created (i.e. the config section has been run) and to continue where left off, or whether a new config needs to be generated in the program
    global configSet
    if configSet == False:
        option = input("\nDo you wish to load in your previous config (logConf.ini)? (Y/N) ")
        if option == "Y" or option == "y":
            configSet = True
            importConfInit()
        elif option == "N" or option == "n":
            configSet = True
            blankConfInit()
        else:
            common.other()

    else:
        menu()

def blankConfInit():
    #Initial Functions - setting up dictionaries with default values (will read config in future)
    #Setup dictionary with default settings for general settings
    global generalSettings
    generalSettings = {"timeinterval": 1,"name": "Default"}
    #Init all objects for 16 channels.
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
    #load menu for the frst time
    menu()

def importConfInit():
    try:
        #Get data from local config file and import (code similar to the logger.py config code)
        global adcDict
        adcDict = {}
        #Open the config file
        config = configparser.ConfigParser()
        config.read('logConf.ini')

        #create dicionry for each item in the general section of the config
        global generalSettings
        generalSettings = {}
        for key in config['General']:
            generalSettings[key] = config['General'][key]

        #For all sections but general, parse the data from config and create a new object for each one and set insance variables for each
        for input in config.sections():
            if input != 'General':
                adcDict[input] = ADC()
                for setting in config[input]:
                    adcDict[input].name = input
                    adcDict[input].enabled = config[input].getboolean('enabled')
                    adcDict[input].inputType = config[input]['inputtype']
                    adcDict[input].gain = config[input].getint('gain')
                    adcDict[input].scaleLow = config[input].getint('scalelow')
                    adcDict[input].scaleHigh = config[input].getint('scalehigh')
                    adcDict[input].unit = config[input]['unit']
        menu()
    except KeyError:
        print("Error Reading Config - Check logConf.ini exists in the same directory as this program")

def menu():
    try:
        while True:
            option = input("\nLogger Config Menu:  \nChoose a Option (based on the correspnding number): \n1. General Settings\n2. Input Setup\n3. Save/Upload Config\n4. Back\n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                general()
            elif option == "2":
                inputSetup()
            elif option == "3":
                saveUpload()
            elif option == "4":
                common.back()
            else:
                common.other()
    except StopIteration:
        pass

#General Settings
#Menu
def general():
    try:
        while True:
            print("\nConfig: General Settings: \nChoose a Option to edit a Setting (based on the correspnding number)")
            x = 0
            for key in generalSettings:
                x+=1
                print("{}. {}: {}".format(x, key, generalSettings[key]))
            print("----------------\n{}. Back\n".format(x+1))
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

#General Time Setting
def generalTime():
    print("\nCurrent Time Interval is: {} Seconds\n".format(generalSettings["Time-Interval"]))
    generalSettings["Time-Interval"] = input("Enter New Time Interval:")
    print("Success\n")

#Name Setting
def generalName():
    print("\nCurrent Name is: {}\n".format(generalSettings["Name"]))
    generalSettings["Name"] = input("Enter New Name:")
    print("Success\n")


#Input Setup (References to above classes which have been created)
def inputSetup():
    inputCurrentSettings()
    chosenPin = input("\nPlease type the Name of Pin (Not the Number) you wish to Edit: ")
    if chosenPin in adcDict:
        #Main menu
        try:
            while True:
                print("\nCurent Pin Settings for: {}\nChoose a Option to edit a Setting (based on the correspnding number)\n1. Pin Enabled: {}\n2. Input Type: {}\n3. Gain: {}\n4. Scale: {} - {}\n5. Unit: {}\n----------------\n6. Back".format(chosenPin,adcDict[chosenPin].enabled,adcDict[chosenPin].inputType,adcDict[chosenPin].gain,adcDict[chosenPin].scaleLow,adcDict[chosenPin].scaleHigh,adcDict[chosenPin].unit))
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
    #Bring up Options for editing
    #Next object

def inputCurrentSettings():
    print("Current Input Settings:\n")
    print("-"*92)
    print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|".format("Number","Name","Pin Enabled","Input Type","Gain","Scale","Unit"))
    print("-"*92)
    x = 0
    for ADC in adcDict:
        x+=1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x,ADC,adcDict[ADC].enabled,adcDict[ADC].inputType,adcDict[ADC].gain,adcDict[ADC].scaleLow,adcDict[ADC].scaleHigh,adcDict[ADC].unit))


#Save/Upload config
def saveUpload():
    try:
        while True:
            print("\nSave/Upload:\nChoose a Option (based on the correspnding number)\n1. Save \n2. Upload \n3. Save and Upload\n4. Back")
            option = input("\nOption Chosen: ")
            if option == "1":
                save()
            elif option == "2":
                upload()
            elif option == "3":
                save()
                upload()
            elif option == "4":
                common.back()
            else:
                common.other()
    except StopIteration:
        pass
def save():
    #Config Setup
    print("\nSaving Config File...")
    logConf = configparser.ConfigParser()

    #Write Sections
    logConf["General"] = {}
    for key in generalSettings:
        logConf["General"][key] = str(generalSettings[key])
    logConf["General"]["uniqueid"] = str(uuid.uuid4())

    #Write data for each A/D
    for key in adcDict:
        logConf[key] = {}
        logConf[key]["enabled"] = str(adcDict[key].enabled)
        logConf[key]["inputtype"] = str(adcDict[key].inputType)
        logConf[key]["gain"] = str(adcDict[key].gain)
        logConf[key]["scalelow"] = str(adcDict[key].scaleLow)
        logConf[key]["scalehigh"] = str(adcDict[key].scaleHigh)
        logConf[key]["unit"] = str(adcDict[key].unit)
    #Write File
    with open('logConf.ini', 'w') as configfile:
        logConf.write(configfile)
    print("Success")
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
            transport.connect(username = username, password = password)
            # Go!
            print("Tranferring Config...")
            sftp = paramiko.SFTPClient.from_transport(transport)
            # Upload
            remotePath = '/home/pi/Github/DataLogger/RPI/logConf.ini'
            localPath = 'logConf.ini'
            sftp.put(localPath, remotePath)
            print("Success")
        finally:
            sftp.close()
            transport.close()
#Temp Code
if __name__ == "__main__":
    init()
