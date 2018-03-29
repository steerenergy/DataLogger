#Import necesarry python files
import sys
#Import local python files for operation
import logCtrl
import about
import processData
import generalSettings

class common:
    #Top 3 are used consistantly in menu system
    def init(self):
        version = "Whatever"
        welcome = "Steer Energy Data Logger (Version {})".format(version)
        print(welcome)
        print("-"*len(welcome))
        main.init(self)

    def quit(self):
        print("\nGoodbye :)\n")
        sys.exit()

    def back(self):
        raise StopIteration()

    def other(self):
        print("Invalid Option. Please Try Again\n")

#Main Menu
class main:
    def init(self):
        try:
            while True:
                option = input("\nMain Menu: \nChoose a Option (based on the correspnding number): \n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit \n\nOption Chosen: ")
                #Set Menu Names
                if option == "1":
                    main.loggerControl(self)
                elif option == "2":
                    main.processData(self)
                elif option == "3":
                    main.generalSettings(self)
                elif option == "4":
                    main.about(self)
                elif option == "5":
                    common.quit(self)
                else:
                    common.other(self)
        except StopIteration:
            pass

    #Top Menu Commands
    def loggerControl(self):
        try:
            while True:
                #Set Menu Names
                option = input("\nLogger Control Menu: \nChoose a Option (based on the correspnding number): \n1. Control (Start/Stop) Logging \n2. Change Logger Config\n3. Download Data \n4. Realtime Data Output \n5. Back \n6. Quit \n\nOption Chosen: ")
                if option == "1":
                    logCtrl.control(self)
                elif option == "2":
                    logCtrl.config(self)
                elif option == "3":
                    logCtrl.downloadData(self)
                elif option == "4":
                    logCtrl.realTime(self)
                elif option == "5":
                    common.back(self)
                elif option =="6":
                    common.quit(self)
                else:
                    common.other(self)
        except StopIteration:
            pass

    def processData(self):
        processData.Download()

    def generalSettings(self):
        try:
            while True:
                option = input("\nGeneral Settings: \nChoose a Option (based on the correspnding number): \n1. Change Language\n2. Back \n3. Quit \nOption Chosen: ")
                #Set Menu Names
                if option == "1":
                    generalSettings.language(self)
                elif option == "2":
                    common.back(self)
                elif option == "3":
                    common.quit(self)
                else:
                    print("\nInvalid Option. Please Try Again")
        except StopIteration:
            pass

    def about(self):
        about.info()

#Program Start
menu = common()
menu.init()
