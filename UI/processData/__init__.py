# Import Common Commands
from processData import process, download, postProcess
import common


# Initial Menu Setup
def init():
    try:
        while True:
            option = input("\nProcess Data Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Download Data\n2. Convert Data\n3. Post Process Data"
                           "\n4. Back\n5. Quit \n\nOption Chosen: ")
            # Set Menu Names
            if option == "1":
                download.init()
            elif option == "2":
                process.init()
            elif option == "3":
                postProcess.init()
            elif option == "4":
                common.back()
            elif option == "5":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass

