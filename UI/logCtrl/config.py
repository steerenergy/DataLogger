#Makes all directory references up a level to simplify importing common files
import sys
sys.path.append("..")
import common

#Initial Functions
def init():
    #Setup dictionary with default settings for general settings
    generalSettings = {"Time-Interval": 0,"Name": "Default"}
    global generalSettings

    menu()

def menu():
    try:
        while True:
            option = input("\nLogger Config: \nChoose a Option (based on the correspnding number): \n1. General Settings\n2. Input Setup \n3. Save/Upload Config \n4. Quit \n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                general()
            elif option == "2":
                pass
            elif option == "3":
                pass
            elif option == "4":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass

def general():
    try:
        while True:
            print("\nConfig: General Settings: \nChoose a Option to edit a Setting (based on the correspnding number)")
            x = 0
            for key in generalSettings:
                x+=1
                print("{}. {}: {}".format(x, key, generalSettings[key]))
            print("----------------\n{}. Back\n{}. Quit".format(x+1,x+2))
            option = input("Option Chosen: ")
            if option == "1":
                generalTime()
            elif option == "2":
                pass
            elif option == "3":
                common.back()
            elif option =="4":
                common.quit()
            else:
                    common.other()
    except StopIteration:
        pass

def generalTime():
    print("\nCurrent Time Interval is: {} Seconds\n".format(generalSettings["Time-Interval"]))
    generalSettings["Time-Interval"] = input("Enter New Time Interval:")
    print("Success\n")
#Temp Code

if __name__ == "__main__":
    init()
