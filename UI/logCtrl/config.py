#Makes all directory references up a level to simplify importing common files
import sys
sys.path.append("..")
import common

#Setting up the Class for the input setup
class ADC:
    def __init__(self):
        self.enabled = False
        self.inputType = "Placeholder"
        self.gain = 0
        self.scale = 0
        self.unit = "Placeholder"

    def enabledEdit():
        pass
    def inputTypeEdit():
        pass
    def gainEdit():
        pass
    def scaleEdit():
        pass
    def unitEdit():
        pass

#Initial Functions - setting up dictionaries with default values (will read config in future)
def init():
    #Setup dictionary with default settings for general settings
    global generalSettings
    generalSettings = {"Time-Interval": 0,"Name": "Default"}
    #Init all objects for 16 channels.
    global adcList
    adcList = {
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

def menu():
    try:
        while True:
            option = input("\nLogger Config: \nChoose a Option (based on the correspnding number): \n1. General Settings\n2. Input Setup \n3. Save/Upload Config \n4. Quit \n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                general()
            elif option == "2":
                inputSetup()
            elif option == "3":
                pass
            elif option == "4":
                common.quit()
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
            print("----------------\n{}. Back\n{}. Quit".format(x+1,x+2))
            option = input("\nOption Chosen: ")
            if option == "1":
                generalTime()
            elif option == "2":
                generalName()
            elif option == "3":
                common.back()
            elif option =="4":
                common.quit()
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
    inputSetupInit()
    #Print All Values for all objects
    #Choose which one to edit
    #Bring up Options for editing
    #Next object

def inputSetupInit():
    print("Current Settings:\n")
    print("-"*79)
    print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|".format("Number","Pin Enabled","Input Type","Gain","Scale","Unit"))
    print("-"*79)
    x = 0
    for ADC in adcList:
        x+=1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|".format(x,adcList[ADC].enabled,adcList[ADC].inputType,adcList[ADC].gain,adcList[ADC].scale,adcList[ADC].unit))


#Temp Code
if __name__ == "__main__":
    init()
