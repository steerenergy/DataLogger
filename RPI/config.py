import configparser
import functools
import Adafruit_ADS1x15
import csv

class ADC:
   def inputSetup(self):
        if self.enabled == True:
            adcToLog.append([self.name,adcPinMap[self.name],'potato'])
        else:
            pass

#Initial Import and setup
def init():

    GAIN = 1
    dataRate = 8
    #A/D Setup - Create 4 instaces of  ADS1115 ADC (16-bit) according to Adafruit Libaries and then assign this to a big list
    adc0 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
    adc1 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
    adc2 = Adafruit_ADS1x15.ADS1115(address=0x4a, busnum=1)
    adc3 = Adafruit_ADS1x15.ADS1115(address=0x4b, busnum=1)

    #Dictionary mapping input pins to physical devices
    global adcPinMap
    adcPinMap ={
    "0A0": functools.partial(adc0.read_adc,0, gain=GAIN, data_rate=dataRate),
    "0A1": functools.partial(adc0.read_adc,1, gain=GAIN, data_rate=dataRate),
    "0A2": functools.partial(adc0.read_adc,2, gain=GAIN, data_rate=dataRate),
    "0A3": functools.partial(adc0.read_adc,3, gain=GAIN, data_rate=dataRate),
    "1A0": functools.partial(adc1.read_adc,0, gain=GAIN, data_rate=dataRate),
    "1A1": functools.partial(adc1.read_adc,1, gain=GAIN, data_rate=dataRate),
    "1A2": functools.partial(adc1.read_adc,2, gain=GAIN, data_rate=dataRate),
    "1A3": functools.partial(adc1.read_adc,3, gain=GAIN, data_rate=dataRate),
    "2A0": functools.partial(adc2.read_adc,0, gain=GAIN, data_rate=dataRate),
    "2A1": functools.partial(adc2.read_adc,1, gain=GAIN, data_rate=dataRate),
    "2A2": functools.partial(adc2.read_adc,2, gain=GAIN, data_rate=dataRate),
    "2A3": functools.partial(adc2.read_adc,3, gain=GAIN, data_rate=dataRate),
    "3A0": functools.partial(adc3.read_adc,0, gain=GAIN, data_rate=dataRate),
    "3A1": functools.partial(adc3.read_adc,1, gain=GAIN, data_rate=dataRate),
    "3A2": functools.partial(adc3.read_adc,2, gain=GAIN, data_rate=dataRate),
    "3A3": functools.partial(adc3.read_adc,3, gain=GAIN, data_rate=dataRate)
    }

    
    global adcToLog
    adcToLog = []
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')
    generalImport()
    inputImport()

#Import General Settings - for now as Global variables
def generalImport():
    global generalSettings
    generalSettings = {}
    for key in config['General']:
        generalSettings[key] = config['General'][key]

    
#Import Input Settings
def inputImport():
    global adcList
    adcList = {}
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
            adcList[input].inputSetup() 

def inputProcess():
    for ADC in adcList:
        adcList[ADC].inputSetup


#Temp Code
def debugOutput():
    x = 0
    for ADC in adcList:
        x+=1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x,adcList[ADC].name,adcList[ADC].enabled,adcList[ADC].inputType,adcList[ADC].gain,adcList[ADC].scaleLow,adcList[ADC].scaleHigh,adcList[ADC].unit))

#Temp testing Code

if __name__ == "__main__":
    init()

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(adcToLog[1][0])
    

    #effective logging code
    for x in range(0,len(adcToLog)):
        print(adcToLog[x][1]())
