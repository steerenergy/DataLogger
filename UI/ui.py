import sys
class Menu:
    def init(self):
        print("Data Logger Pre Release")
        print("-"*50,'\n')
        menu.main()

    def main(self):
        #Main Menu
        while True:
            option = input("Main Menu: \nChoose a Option (based on the correspnding number): \n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit \nOption: ")
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

    def loggerControl(self):
        print("\nOption 1\n")

    def processData(self):
        print("\nOption 2\n")

    def generalSettings(self):
        print("\nOption 3\n")

    def about(self):
        print("\nOption 4\n")

    def quit(self):
        print("\nGoodbye\n")
        sys.exit()

#Program Start
menu = Menu()
menu.init()
