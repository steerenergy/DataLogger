#Import Time for Delay functions etc
import time;
#Import datetime for Logging
from datetime import datetime
# Import the ADS1x15 module.
import Adafruit_ADS1x15;
#Import CSV Logging Module
import csv;

# Create 4 instaces of  ADS1115 ADC (16-bit) according to Adafruit Libaries. These are placed into a table
adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1);
adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1);
adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1);
adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1);
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
GAIN = 1;
#Max Raw Data Value (15 bit)/Max voltage. Finds how many mV 1 bit represents. Note if gain is adjusted this will also need to be changed.
voltageConvert = 4096.0/32767.0;
#set up list to be printed
adcValues = [0,0,0,0];
#Chooses which A/D convertor is selected by default
#n = ADC unit number - 0 is first unit 3 is 4th unit etc.
n = 0
#Choose data rate (must be certain value see datasheet/documentaion for more)
dataRate=860

time.sleep(1);
with open('voltage.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL);
    print("Beginning Test...");
    writer.writerow(["Date/Time","A/D Unit","A0 (mV)","A1 (mV)","A2 (mV)","A3 (mV)"]);
    while(True):
        #Print current A/D selected - from 0 to 3
        print("Reading Begin | Current A/D Selected:",n)
        print("-" *53,"\n");
        for currentPin in range(4):
            print("Current Pin: Pin A" + str(currentPin));
            #Prints raw data from the A/D convertion , straight from the I2C Bus
            raw = adcUnit[n].read_adc(currentPin, gain=GAIN, data_rate=dataRate);
            print("Raw Data:", raw);
            #Converted to voltage using above conversion variable (voltageConvert)
            voltage = (raw * voltageConvert);
            print("Voltage:", round(voltage,2), "mV \n");
            #set voltage to value in table
            adcValues[currentPin] = voltage;
        #Get time and send to log Log
        currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S");
        #Export Data to Spreadsheet and Reset list values (so we can see if code fails)
        writer.writerow([currentDateTime] + [n] + adcValues);
        adcValues = [0,0,0,0];

        #Select next A/D convertor
        if n == 3:
            n = 0;
        else:
            n = n + 1;
