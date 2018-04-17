#Import Common Comands
import sys
sys.path.append("..")
import common
from logCtrl import config

def init():
    try:
        while True:
            #Set Menu Names
            option = input("\nLogger Control Menu: \nChoose a Option (based on the correspnding number): \n1. Control (Start/Stop) Logging \n2. Change Logger Config\n3. Download Data \n4. Realtime Data Output \n5. Back \n6. Quit \n\nOption Chosen: ")
            if option == "1":
                control()
            elif option == "2":
                config.init()
            elif option == "3":
                downloadData()
            elif option == "4":
                realTime()
            elif option == "5":
                common.back()
            elif option =="6":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass



#Logger Control Comands
def control():
    pass
def downloadData():
    pass
def realTime():
    print("\nComing Soon!\n")
