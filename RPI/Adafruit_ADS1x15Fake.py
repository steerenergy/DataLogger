# NOTE - DELETE/Rename WHEN RUNNING ON PI!
# This script is for testing code when the pis isn't available
# It will simply return a number regardless of the pin
import time
import random

x = 0


class ADS1115:

    def __init__(self, address, busnum):
        self.address = address
        self.busNum = busnum

    def read_adc(self, pin, gain, data_rate):
        global x
        if pin == 0:
            x = x + 1
        time.sleep(0.05)
        # return "P:{} N{}".format(pin, x)
        return random.randint(0, 32767)
