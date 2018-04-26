# Main Menu - Initialised by UI.py and creates main menu linking to other imported modules

# Import local python files for operation
import common
import logCtrl
import about
import processData
import generalSettings


# Printed Title
def init():
    version = "Whatever"
    welcome = "Steer Energy Data Logger (Version {})".format(version)
    print(welcome)
    print("-" * len(welcome))
    main()


# Main Menu - Structure very similar to other menus.
def main():
    try:
        while True:
            option = input(
                "\nMain Menu: \nChoose a Option (based on the corresponding number):"
                "\n1. Logger Control\n2. Process Data \n3. General Settings \n4. About \n5. Quit" 
                "\n\nOption Chosen: ")
            # Set Menu Names
            if option == "1":
                logCtrl.init()
            elif option == "2":
                processData.init()
            elif option == "3":
                generalSettings.init()
            elif option == "4":
                about.init()
            elif option == "5":
                common.quit()
            else:
                common.other()
    # Used to break the loop if someone selects a back option.
    # No back option as this is root menu: this is left here for sake of consistency with other menus.
    except StopIteration:
        pass
