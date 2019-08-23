# Main Menu - Initialised by UI.py and creates main menu linking to other imported modules

# Import local python files for operation
import common
import logCtrl
import about
import processData
import generalSettings
import ctypes


# Title printed on program start
def init():
    version = "1.1.0 Alpha"
    # Set Windows Title
    welcome = "Steer Energy Data Logger (Version {})".format(version)
    ctypes.windll.kernel32.SetConsoleTitleW(welcome)
    print(welcome)
    print("-" * len(welcome))
    # Initiate main menu
    main()


# Main Menu - Structure very similar to all other menus in program
def main():
    try:
        while True:
            option = input(
                "\nMain Menu: \nChoose a Option (based on the corresponding number):"
                "\n1. Logger Control (Config)\n2. Process Data \n3. General Settings \n4. About \n5. Quit" 
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
