#Import Time for Delay functions etc
import time
#Import datetime for Logging
from datetime import datetime
# Import the ADS1x15 module.
import Adafruit_ADS1x15
#Import CSV Logging Module
import csv

# Create 4 instaces of  ADS1115 ADC (16-bit) according to Adafruit Libaries. These are placed into a table
adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)
adcUnit = [adc0,adc1,adc2,adc3]

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
#Max Raw Data Value (15 bit)/Max voltage. Finds how many mV 1 bit represents. Note if gain is adjusted this will also need to be changed.
voltageConvert = 4096.0/32767.0
#set up list to be printed
adcValues = [0,0,0,0]
#Chooses which A/D convertor is selected by default
#n = ADC unit number - 0 is first unit 3 is 4th unit etc.
n = 0
#Choose data rate (must be certain value see datasheet/documentaion for more)
dataRate=860

#First Line intro
print("Python Data Logger")
#Ask user for frequency of logging
timeDelay = float(input("How many seconds between each log?\n"))

time.sleep(0.5)

try:
    with open('voltage.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("Logging Begin")
        writer.writerow(["Date/Time","A/D Unit","A0 (mV)","A1 (mV)","A2 (mV)","A3 (mV)"])

        #Set startime
        starttime=time.time()

        while(True):

            #Print current A/D selected - from 0 to 3
            #print("Reading Begin | Current A/D Selected:",n)
            #print("-" *53,"\n");
            for currentPin in range(4):
                #Get Raw data from A/D, convert to voltage and add to adcValues list corresponding to the current pin
                raw = adcUnit[n].read_adc(currentPin, gain=GAIN, data_rate=dataRate)
                adcValues[currentPin] = (raw * voltageConvert)
                #Optional Debugging Print Statements - Uncomment to Use
                #print("Current Pin: Pin A" + str(currentPin))
                #print("Raw Data:", raw);
                #print("Voltage:", round(adcValues[currentPin],2), "mV \n")
            #Get time and send to log Log
            currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S %f");
            #Export Data to Spreadsheet and Reset list values (so we can see if code fails)
            writer.writerow([currentDateTime] + [n] + adcValues)
            adcValues = [0,0,0,0]

            #Select next A/D convertor
            if n == 3:
                n = 0
                #Work out time delay needed until next set of values taken based on user given value (using some clever maths)
                time.sleep(timeDelay - ((time.time() - starttime) % timeDelay))
            else:
                n = n + 1


except KeyboardInterrupt:
       print("Logging Finished") 
