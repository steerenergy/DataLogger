import configparser


class ADC:
    pass
   # def setup(self):
        #if self.enabled =

#Initial Import
def init():
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
                adcList[input].enabled = config[input].getboolean('enabled')
                adcList[input].inputType = config[input]['inputtype']
                adcList[input].gain = config[input].getint('gain')
                adcList[input].scaleLow = config[input].getint('scalelow')
                adcList[input].scaleHigh = config[input].getint('scalehigh')
                adcList[input].unit = config[input]['unit']
    debugOutput()
def debugOutput():
    x = 0
    for ADC in adcList:
        x+=1
        print("|{:>12}|{:>12}|{:>12}|{:>12}|{:>12}|{:>6}{:>6}|{:>12}|".format(x,ADC,adcList[ADC].enabled,adcList[ADC].inputType,adcList[ADC].gain,adcList[ADC].scaleLow,adcList[ADC].scaleHigh,adcList[ADC].unit))
def inputProcess():
    for ADC in adcList:
        adcList[ADC].setup


#Temp testing Code

if __name__ == "__main__":
    init()
