#Makes all directory references up a level to simplify importing common files
import sys
sys.path.append("..")
#Import Common Comands
import common


def init():
    try:
        while True:
            option = input("\nProcess Data Menu: \nChoose a Option (based on the correspnding number): \n1. Download\n2. Process\n3.Back\n4. Quit \n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                download()
            elif option == "2":
                process()
            elif option == "3":
                common.back()
            elif option == "4":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass

if __name__ == "__main__":
    init()
