import numpy as np
import pandas as pd
import sys
import configparser
sys.path.append("..")
import common

#Functiosn for calculating conversions in csv
def gain(gain):
    #Table of Gain to voltage convert adcValues. Voltage is in volts
    return gainList[gain]/32767.0

def scale(scaleLow,scaleHigh,inputType):
    #Effectively usign y = mx+c
    #Scale on Y, inputType on x)
    inputLow = inputTypeList[inputType][0]
    inputHigh = inputTypeList[inputType][1]
    m = (scaleHigh-scaleLow)/(inputHigh-inputLow)
    c = scaleHigh-m*inputHigh
    return(m,c)


def init():
    global conversion
    conversion = {}

    #Setup of gain/type.scale for conversion
    global gainList
    gainList = {
    1:4.096,
    2:2.04,
    4:1.024,
    8:0.512,
    16:0.256
    }
    #Input type list: contains a tuple with the value (in volts) for the low end of the scale, and the value for the high end of the scale
    global inputTypeList
    inputTypeList = {
    "4-20":(0.4,2),
    "0-2V": (0,2)
}
    conversionSetup()
    csvProcess()

def conversionSetup():
    #Load Config
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')
    for key in config.sections():
        if key != 'General' and config[key].getboolean('enabled') == True:
            #Get values of m and c in y = mx+c
            m,c = scale(config[key].getint('scalelow'),config[key].getint('scalehigh'),config[key]['inputtype'])
            #Use y = mx+c to find conversion value. This finds the conversion factor from raw data to the scale chosen
            conversion[key] = m*gain(config[key].getint('gain')) + c

def convert(value,item):
    return value*conversion[item]

def csvProcess():
    #read CSV
    df = pd.read_csv('raw.csv')
    print("Raw Data:")
    print(df)
    for item in df.iloc[:,2:].columns:
        df[item] = df[item].apply(convert, args=(item,))
        df.rename(columns={item: item + " " + config[item]['unit']}, inplace=True)
    print("\nConverted Data:")
    print(df)
    #Write Converted CSV
    df.to_csv('converted.csv', sep=',')




if __name__ == "__main__":
    init()
