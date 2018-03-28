import sys
class Menu:
    def init(self):
        print("Data Logger Pre Release")
        print("-"*50,'\n')
        menu.main()

    def main(self):
        #Main Menu
        while True:
            option = input("Main Menu: \nChoose a Option (based on the correspnding number): \n1. Option 1 \n2. Option 2 \n3. Option 3 \n4. Exit \nOption: ")
            #Set Menu Names
            if option == "1":
                menu.option1()
            elif option == "2":
                menu.option2()
            elif option == "3":
                menu.option3()
            elif option == "4":
                menu.option4()
            else:
                print("Invalid Option. Please Try Again\n")

    def option1(self):
        print("\nOption 1\n")
    def option2(self):
        print("\nOption 2\n")
    def option3(self):
        print("\nOption 3\n")
    def option4(self):
        print("\nGoodbye\n")
        sys.exit()

#Program Start
menu = Menu()
menu.init()
