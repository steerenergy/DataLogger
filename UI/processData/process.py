# One of the main files in the UI script. Handles the reading of the CSV and config file and processing the data.
# Program begins at init() which creates variables and imports the datatype lists.
# This calls conversionSetup() which loads in the pre calculated m and c values (in y = mx + c).
# These are stored in the 'conversion' list as a tuple
# Then csvProcess is called which loads the csv and performs the convert() on each cell efficiently via pandas
# A converted CSV is then written

# Import Stuff
import pandas as pd
import sys
import configparser

sys.path.append("..")


# Function called by csvProcess which does the actual data conversion on each data item
def convert(value, item):
    return value * conversion[item][0] + conversion[item][1]


# General init functions - including gain list setup and loading in program config
def init():
    # Create Dicts/Vars
    # Conversion contains m and c values used for converting raw data to real values
    global conversion
    conversion = {}

    # Start conversion process
    conversionSetup()
    csvProcess()


# Importing the information from the config file and creating a dictionary for m and c values needed for data conversion
def conversionSetup():
    # Load Config from File
    global config
    config = configparser.ConfigParser()
    config.read('logConf.ini')
    # Process config for all enabled channels in config file
    for key in config.sections():
        if key != 'General' and config[key].getboolean('enabled') is True:
            # Get values of m and c (in y = mx + c) from config
            conversion[key] = (config[key].getfloat('m'), config[key].getfloat('c'))


# Loading CSV into pandas, processing the data and exporting converted CSV
def csvProcess():
    # Read CSV file
    df = pd.read_csv('raw.csv')
    print("Raw Data (Top Lines):")
    print(df.head())
    # Data Conversion Loop
    print("\nConverting Data...")
    # Skip first 2 columns (Data/Time and Time Interval) and iterate each column thereafter
    for item in df.iloc[:, 2:].columns:
        # Below line runs convert function on each row in column
        df[item] = df[item].apply(convert, args=(item,))
        # Rename Column heading to add Units onto the end of them
        df.rename(columns={item: item + " " + config[item]['unit']}, inplace=True)
    # Print out Result
    print("\nConverted Data (Top Lines):")
    print(df.head())
    # Write Converted CSV Data
    print("\nWriting CSV...")
    df.to_csv('converted.csv', sep=',', index=False)
    print("\nSuccess")


if __name__ == "__main__":
    init()
