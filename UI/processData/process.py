# One of the main files in the UI script. Handles the reading of the CSV and config file and processing the data.
# Program begins at init() which creates variables and imports the datatype lists.
# This calls conversionSetup() which loads the logConf.ini file and generates scale factors from this.
# The scale factor is stored as a m and c term (in y = mx + c) waiting to be used
# Then csvProcess is called which loads the csv and performs the conversion operation on each column and row.
# A converted CSV is then written

# Import Stuff
import pandas as pd
import sys
import configparser
sys.path.append("..")


# Functions for calculating conversions in csv
def gain(gain):
    # Table of Gain to voltage convert adcValues. Voltage is in volts
    return gainList[gain]/32767.0


def scale(scaleLow, scaleHigh, inputType):
    # Effectively using y = mx+c
    # Scale on y, inputType on x)
    inputLow = inputTypeDict[inputType][0]
    inputHigh = inputTypeDict[inputType][1]
    m = (scaleHigh-scaleLow)/(inputHigh-inputLow)
    c = scaleHigh-m*inputHigh
    return m, c


def convert(value,item):
    return value*conversion[item][0] + conversion[item][1]


def init():
    # Create Dicts/Vars
    global conversion
    conversion = {}
    # Setup of gain/type.scale for conversion
    global gainList
    gainList = {
    1:4.096,
    2:2.04,
    4:1.024,
    8:0.512,
    16:0.256
    }
    # Input type list: contains a tuple with the value (in volts) for the low and high end of the scale
    # Create config object, make it preserve case on import and read config file
    progConf = configparser.ConfigParser()
    progConf.optionxform = str
    progConf.read('progConf.ini')
    global inputTypeDict
    inputTypeDict = {}
    for key in progConf['inputTypes']:
        inputTypeDict[key] = eval(progConf['inputTypes'][key])

    conversionSetup()
    csvProcess()


def conversionSetup():
    # Load Config from File
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')
    for key in config.sections():
        if key != 'General' and config[key].getboolean('enabled') is True:
            # Get values of m and c in y = mx+c by passing config data to scale() function
            m,c = scale(config[key].getint('scalelow'),config[key].getint('scalehigh'),config[key]['inputtype'])
            # Use y = mx+c to find conversion value. This finds the conversion factor from raw data to the scale chosen
            m = m*gain(config[key].getint('gain'))
            conversion[key] = (m,c)


def csvProcess():
    # Read CSV file
    df = pd.read_csv('raw.csv')
    print("Raw Data (Top Lines):")
    print(df.head())
    # Data Conversion Loop
    print("\nConverting Data...")
    # Skip first 2 columns (Data/Time and Time Interval) and iterate each column thereafter
    for item in df.iloc[:,2:].columns:
        # Below line runs convert function on each row in column
        df[item] = df[item].apply(convert, args=(item,))
        # Rename Column heading to add Units onto the end of them
        df.rename(columns={item: item + " " + config[item]['unit']}, inplace=True)
    # Print out Result
    print("\nConverted Data (Top Lines):")
    print(df.head())
    # Write Converted CSV Data
    print("\nWriting CSV...")
    df.to_csv('converted.csv', sep=',', index = False)
    print("\nSuccess")


if __name__ == "__main__":
    init()
