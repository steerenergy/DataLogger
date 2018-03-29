#Import Common Comands
import common

def init():
    try:
        while True:
            option = input("\nGeneral Settings: \nChoose a Option (based on the correspnding number): \n1. Change Language\n2. Back \n3. Quit \nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                language()
            elif option == "2":
                common.back()
            elif option == "3":
                common.quit()
            else:
                print("\nInvalid Option. Please Try Again")
    except StopIteration:
        pass

def language():
    print("\nEnglish Only\n")
