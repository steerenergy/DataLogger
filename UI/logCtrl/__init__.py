# Creates menu allowing user to choose different log control options
# This menu doesn't really do much and at some point should be removed.

# Import Common Commands
import common
from logCtrl import config


def init():
    try:
        while True:
            # Set Menu Names
            option = input("\nLogger Control Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Change Logger Configuration"
                           "\n2. Back\n3. Quit"
                           "\n\nOption Chosen: ")
            if option == "1":
                config.init()
            elif option == "2":
                common.back()
            elif option == "3":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass
