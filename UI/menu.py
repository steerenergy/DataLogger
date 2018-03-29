#Import necesarry python files
import sys
#Import local python files for operation
import logCtrl
import about
import processData
import generalSettings
import common

#Initial
def init():
    version = "Whatever"
    welcome = "Steer Energy Data Logger (Version {})".format(version)
    print(welcome)
    print("-"*len(welcome))
    main()



#Main Menu
def main():
    try:
        while True:
            option = input("\nMain Menu: \nChoose a Option (based on the correspnding number): \n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit \n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                logCtrl.init()
            elif option == "2":
                processData.init()
            elif option == "3":
                generalSettings.init()
            elif option == "4":
                about.init()
            elif option == "5":
                quit()
            else:
                other()
    except StopIteration:
        pass
