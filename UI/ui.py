import sys
class Menu:
    #Top 3 are used consistantly in menu system
    def init(self):
        print("Data Logger Pre Release Version Whatver")
        print("-"*50,'')
        menu.main()

    def quit(self):
        print("\nGoodbye\n")
        sys.exit()

    def back(self):
        raise StopIteration()

    #Main Menu
    def main(self):
        #Main Menu
        try:
            while True:
                option = input("\nMain Menu: \nChoose a Option (based on the correspnding number): \n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit \nOption Chosen: ")
                #Set Menu Names
                if option == "1":
                    menu.loggerControl()
                elif option == "2":
                    menu.processData()
                elif option == "3":
                    menu.generalSettings()
                elif option == "4":
                    menu.about()
                elif option == "5":
                    menu.quit()
                else:
                    print("Invalid Option. Please Try Again\n")
        except StopIteration:
            pass

    #Top Menu Comands
    def loggerControl(self):
        try:
            while True:
                option = input("\nLogger Control Menu: \nChoose a Option (based on the correspnding number): \n1. Change Logger Config\n2. Download Data \n3. Realtime Data Output \n4. Back \n5. Quit \nOption Chosen: ")
                #Set Menu Names
                if option == "1":
                    menu.loggerConfig()
                elif option == "2":
                    menu.downloadData()
                elif option == "3":
                    menu.realtimeData()
                elif option == "4":
                    menu.back()
                elif option == "5":
                    menu.quit()
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

    #Logger Control Comands
    def loggerConfig(self):
        pass
    def downloadData(self):
        pass
    def realtimeData(self):
        print("\nComing Soon!\n")

#Program Start
menu = Menu()
menu.init()
