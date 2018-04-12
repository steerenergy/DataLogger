#Import Libaries
import time
from datetime import datetime
import configparser
import functools
import Adafruit_ADS1x15
import csv

class ADC:
   def inputSetup(self):
        if self.enabled == True:
            adcToLog.append(adcPinMap[self.name])
            adcHeader.append([self.name,self.inputType,self.gain,self.scaleLow,self.scaleHigh,self.unit])
        else:
            pass

#Initial Import and setup
def init():
    #Setting up key variables
    global dataRate
    dataRate = 8
    global adcToLog
    adcToLog = []
    global adcHeader
    adcHeader = []
    global adcList
    adcList = {}
    #A/D Setup - Create 4 instaces of  ADS1115 ADC (16-bit) according to Adafruit Libaries and then assign this to a big list
    global adc0
    global adc1
    global adc2
    global adc3
    adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
    adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
    adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)

    #Dictionary mapping input pins to physical devices
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')

    generalImport()

    inputImport()
#Import General Settings - for now as Global variables
def generalImport():
   print("Configuring General Settings")
    global generalSettings
    generalSettings = {}
    for key in config['General']:
        generalSettings[key] = config['General'][key]
      

    
#Import Input Settings
def inputImport():
    print("Configuring Input Settings")
    for input in config.sections():
        if input != 'General':
            adcList[input] = ADC()
            for setting in config[input]:
                adcList[input].name = input
                adcList[input].enabled = config[input].getboolean('enabled')
                adcList[input].inputType = config[input]['inputtype']
                adcList[input].gain = config[input].getint('gain')
                adcList[input].scaleLow = config[input].getint('scalelow')
                adcList[input].scaleHigh = config[input].getint('scalehigh')
                adcList[input].unit = config[input]['unit']
    #ADC Pin Map List
    global adcPinMap
    adcPinMap ={
    "0A0": functools.partial(adc0.read_adc,0, gain=adcList["0A0"].gain, data_rate=dataRate),
    "0A1": functools.partial(adc0.read_adc,1, gain=adcList["0A1"].gain, data_rate=dataRate),
    "0A2": functools.partial(adc0.read_adc,2, gain=adcList["0A2"].gain, data_rate=dataRate),
    "0A3": functools.partial(adc0.read_adc,3, gain=adcList["0A3"].gain, data_rate=dataRate),
    "1A0": functools.partial(adc1.read_adc,0, gain=adcList["1A0"].gain, data_rate=dataRate),
    "1A1": functools.partial(adc1.read_adc,1, gain=adcList["1A1"].gain, data_rate=dataRate),
    "1A2": functools.partial(adc1.read_adc,2, gain=adcList["1A2"].gain, data_rate=dataRate),
    "1A3": functools.partial(adc1.read_adc,3, gain=adcList["1A3"].gain, data_rate=dataRate),
    "2A0": functools.partial(adc2.read_adc,0, gain=adcList["2A0"].gain, data_rate=dataRate),
    "2A1": functools.partial(adc2.read_adc,1, gain=adcList["2A1"].gain, data_rate=dataRate),
    "2A2": functools.partial(adc2.read_adc,2, gain=adcList["2A2"].gain, data_rate=dataRate),
    "2A3": functools.partial(adc2.read_adc,3, gain=adcList["2A3"].gain, data_rate=dataRate),
    "3A0": functools.partial(adc3.read_adc,0, gain=adcList["3A0"].gain, data_rate=dataRate),
    "3A1": functools.partial(adc3.read_adc,1, gain=adcList["3A1"].gain, data_rate=dataRate),
    "3A2": functools.partial(adc3.read_adc,2, gain=adcList["3A2"].gain, data_rate=dataRate),
    "3A3": functools.partial(adc3.read_adc,3, gain=adcList["3A3"].gain, data_rate=dataRate)
    } 
    for adc in adcList:
       adcList[adc].inputSetup()
#Temp Code
def debugOutput():
    x = 0
    for ADC in adcList:
        x+=1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x,adcList[ADC].name,adcList[ADC].enabled,adcList[ADC].inputType,adcList[ADC].gain,adcList[ADC].scaleLow,adcList[ADC].scaleHigh,adcList[ADC].unit))

def csvConf():
   with open('/home/pi/Github/DataLogger/RPI/voltage.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, dialect="excel", delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["Name:",generalSettings['name'],"ID:",generalSettings['uniqueid'],"Time Interval",generalSettings['timeinterval']])
      writer.writerows(zip(*adcHeader))

if __name__ == "__main__":
   #Load Config Data
   init()
   #Write CSV Header
   csvConf()
