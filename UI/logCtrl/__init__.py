#Import Common Comands
import sys
sys.path.append("..")
import common
from logCtrl import config

def init():
    try:
        while True:
            #Set Menu Names
            option = input("\nLogger Control Menu: \nChoose a Option (based on the correspnding number): \n1. Control (Start/Stop) Logging\n2. Change Logger Config\n3. Realtime Data Output\n4. Back\n5. Quit\n\nOption Chosen: ")
            if option == "1":
                control()
            elif option == "2":
                config.init()
            elif option == "3":
                realTime()
            elif option == "4":
                common.back()
            elif option =="5":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass



#Logger Control Comands
def control():
    print("\n Remote Control Coming Soon! \n Once the config is uploaded to the RPI, please start the program manually on the pi itself.")
#Future Realtime Data Code
def realTime():
    print("\nComing Soon!\n")
