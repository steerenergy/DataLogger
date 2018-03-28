#import necesarry files
import sys
import logCtrl

class common:
    #Top 3 are used consistantly in menu system
    def init(self):
        print("Data Logger Pre Release Version Whatver")
        print("-"*50,'')
        main.init(self)

    def quit(self):
        print("\nGoodbye\n")
        sys.exit()

    def back(self):
        raise StopIteration()

#Main Menu
class main:
    def init(self):
        try:
            while True:
                option = input("\nMain Menu: \nChoose a Option (based on the correspnding number): \n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit \nOption Chosen: ")
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
                    print("Invalid Option. Please Try Again\n")
        except StopIteration:
            pass

    #Top Menu Commands
    def loggerControl(self):
        try:
            while True:
                option = input("\nLogger Control Menu: \nChoose a Option (based on the correspnding number): \n1. Change Logger Config\n2. Download Data \n3. Realtime Data Output \n4. Back \n5. Quit \nOption Chosen: ")
                #Set Menu Names
                if option == "1":
                    logCtrl.config(self)
                elif option == "2":
                    logCtrl.downloadData(self)
                elif option == "3":
                    logCtrl.realTime(self)
                elif option == "4":
                    common.back(self)
                elif option == "5":
                    common.quit(self)
                else:
                    print("Invalid Option. Please Try Again\n")
        except StopIteration:
            pass

    def processData(self):
        print("\nOption 2\n")

    def generalSettings(self):
        print("\nOption 3\n")

    def about(self):
        print("\nOption 4\n")

#Program Start
menu = common()
menu.init()
