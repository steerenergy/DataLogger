# Placeholder for future settings

# Import Common Commands
import common


# Main Menu
def init():
    try:
        while True:
            option = input("\nGeneral Settings: \nChoose a Option (based on the corresponding number):" 
                           "\n1. Change Language\n2. Back\n3. Quit"
                           "\n\nOption Chosen: ")
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


# Language Settings
def language():
    print("\nEnglish Only\n")
