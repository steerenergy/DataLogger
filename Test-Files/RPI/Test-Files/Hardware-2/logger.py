#Import Libaries
import time
from datetime import datetime
import Adafruit_ADS1x15
import csv
import functools
#Variables

# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
#Choose data rate (must be certain value see datasheet/documentaion for more)
dataRate=860
#Max Raw Data Value (15 bit)/Max voltage. Finds how many mV 1 bit represents. Note if gain is adjusted this will also need to be changed.
voltageConvert = 4096.0/32767.0
#Set up list to be printed to CSV
adcValues = [0]*4


#A/D Setup - Create 4 instaces of  ADS1115 ADC (16-bit) according to Adafruit Libaries and then assign this to a big list
adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)

<<<<<<< HEAD:RPI/logger.py

adcPinRead =[functools.partial(adc0.read_adc,0, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,1, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,2, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,3, gain=GAIN, data_rate=dataRate),\
functools.partial(adc1.read_adc,0, gain=GAIN, data_rate=dataRate),\
functools.partial(adc1.read_adc,1, gain=GAIN, data_rate=dataRate),\
functools.partial(adc1.read_adc,2, gain=GAIN, data_rate=dataRate),\
functools.partial(adc1.read_adc,3, gain=GAIN, data_rate=dataRate),\
functools.partial(adc2.read_adc,0, gain=GAIN, data_rate=dataRate),\
functools.partial(adc2.read_adc,1, gain=GAIN, data_rate=dataRate),\
functools.partial(adc2.read_adc,2, gain=GAIN, data_rate=dataRate),\
functools.partial(adc2.read_adc,3, gain=GAIN, data_rate=dataRate),\
functools.partial(adc3.read_adc,0, gain=GAIN, data_rate=dataRate),\
functools.partial(adc3.read_adc,1, gain=GAIN, data_rate=dataRate),\
functools.partial(adc3.read_adc,2, gain=GAIN, data_rate=dataRate),\
functools.partial(adc3.read_adc,3, gain=GAIN, data_rate=dataRate)]
=======
>>>>>>> Hardware-2:RPI/Test-Files/Hardware-2/logger.py

adcPinRead =[functools.partial(adc0.read_adc,0, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,1, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,2, gain=GAIN, data_rate=dataRate),\
functools.partial(adc0.read_adc,3, gain=GAIN, data_rate=dataRate)]
#Process Begin
#First Line intro
print("Python Data Logger")
#Set Frequency of Logging
<<<<<<< HEAD:RPI/logger.py
timeInterval = 1
=======
timeInterval = 0.05
>>>>>>> Hardware-2:RPI/Test-Files/Hardware-2/logger.py

#Try is for error handlng
try:
    #CSV setup
    with open('/home/pi/Github/DataLogger/RPI/voltage.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Date/Time","Time Elapsed (Seconds)","0A0 (mV)","0A1 (mV)","0A2 (mV)","0A3 (mV)"])

        #Logging Process beginning

        #Syncing clock up to try and centre values
        print("Syncing Clock")
        begin = time.perf_counter()
        while ((time.perf_counter()-begin) % timeInterval) < (timeInterval/2):
            pass

        print("Logging Begin\n")

        #Set startTime (method used ignores changes in system clock time)
        startTime=time.perf_counter()

        #Beginning of reading script
        while(True):
            #Get time and send to Log
            currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f");
            timeElapsed = round(time.perf_counter() - startTime,4)

            #REqrite using Enumerate (unpack the tuple)
<<<<<<< HEAD:RPI/logger.py
            for currentPin in range(16):
=======
            for currentPin in range(4):
>>>>>>> Hardware-2:RPI/Test-Files/Hardware-2/logger.py
                #Get Raw data from A/D, convert to voltage and add to adcValues list corresponding to the current pin
                adcValues[currentPin] = (adcPinRead[currentPin]() * voltageConvert)
            
            #Export Data to Spreadsheet inc current datetime and time elasped and Reset list values (so we can see if code fails)
            writer.writerow([currentDateTime] + [timeElapsed] + adcValues)
            adcValues = [0]*4
            #Work out time delay needed until next set of values taken based on user given value (using some clever maths)
            timeDiff=(time.perf_counter() - startTime)
            time.sleep(timeInterval - (timeDiff % timeInterval))
except KeyboardInterrupt:
       print("Logging Finished")
