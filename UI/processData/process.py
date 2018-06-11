# One of the main files in the UI script. Handles the reading of the CSV and config file and processing the data.
# Program begins at init() creating the conversion list, creates an instance of fileSelect and trggers main functions
# The File select constructor (__init__) calls the other functions dealing with selecting the CSV and logConf file
# This creates variables which are used for loading in files.
# init() then calls conversionSetup() which loads in the pre calculated m and c values (in y = mx + c).
# These are stored in the 'conversion' list as a tuple
# Then csvProcess is called which loads the csv and performs the convert() on each cell efficiently via pandas
# A converted CSV is then written in the data directory. The other files are then move to the same location

# Import Stuff
import pandas as pd
import configparser
import os
import common


class fileSelect:
    def __init__(self):
        # Declaring all variables needed
        self.inboxDirectory = 'files/inbox'
        self.dataDirectory = 'files/data'
        self.inboxContents = os.listdir(self.inboxDirectory)
        self.rawCsvFiles = []
        self.configFiles = []
        self.fileSelection = []
        self.chosenID = None
        self.rawCsvFile = None
        self.configFile = None
        self.convertedCsvFile = None
        self.rawCsvFilePath = None
        self.configFilePath = None
        self.convertedCsvFilePath = None
        # Run file selection and linking methods
        self.fileLink()
        self.fileSelect()
        self.filePathLinker()

    # Links the CSV and Config Files Together
    def fileLink(self):
        # Using List Comprehension - create a list of csvFiles and configFiles
        self.rawCsvFiles = [fileName for fileName in self.inboxContents if fileName.endswith('.csv')]
        self.configFiles = [fileName for fileName in self.inboxContents if fileName.endswith('.ini')]

        # Link a CSV file to a Config File
        for rawCsvFile in self.rawCsvFiles:
            # Strip the filename to just the timestamp
            timeStamp = rawCsvFile[len('raw'):-len('.ini')]
            # Match with a configFile
            # matchFound used to print error message if no match is found
            matchFound = False
            for configFile in self.configFiles:
                if timeStamp in configFile:
                    self.fileSelection.append((timeStamp, rawCsvFile, configFile))
                    # Remove config file from list as it doesn't need to be searched again on next iteration
                    self.configFiles.remove(configFile)
                    # Change matchFound flag to rue
                    matchFound = True
                    break
            # Error which shows if there was not a match
            if matchFound is False:
                print("\nERROR - Unable to find matching config for '{}'. Please check the '/files/inbox' folder"
                      .format(self.rawCsvFile))

    # Allows user to choose which files they want
    def fileSelect(self):
        # Dealing with cases where there are no matching files in directory
        if len(self.fileSelection) <= 0:
            print("\nNo Data Found - Please ensure there is at least 1 matching raw.csv and logConf.ini file "
                  "inside the inbox directory.")
            common.back()
        else:
            # Print the data found in the folder
            print("\nData Found \nThe file's datestamps are shown below:")
            for pos, value in enumerate(self.fileSelection, start=1):
                print("{}. {}".format(pos, value[0]))
            # Option Selection
            try:
                option = int(input("\nSelect a file by its corresponding number: "))
                # Check to see value can be chosen - note the numbers listed start at 1 but lists in python start at 0
                if 0 < option <= len(self.fileSelection):
                    # Setting the filenames - note these are not the complete file paths
                    self.chosenID = self.fileSelection[option-1][0]
                    self.rawCsvFile = self.fileSelection[option-1][1]
                    self.configFile = self.fileSelection[option-1][2]
                    # Works out filename for converted CSV file
                    self.convertedCsvFile = "converted" + self.chosenID + ".csv"
                    print("Success!")
                else:
                    common.other()
                    common.back()
            # If someone does not put in an integer
            except ValueError:
                common.other()
                common.back()

    # Sets file path var for each file in question
    def filePathLinker(self):
        self.rawCsvFilePath = self.inboxDirectory + "/" + self.rawCsvFile
        self.configFilePath = self.inboxDirectory + "/" + self.configFile

    # Moves raw and config files that have just been processed into the data directory (where the converted csv is)
    def fileCleanup(self):
        print("Moving Files...")
        # Converted CSV data is already in the correct place so just need to move raw data and config
        os.rename(self.configFilePath,self.dataDirectory + '/' + self.configFile)
        os.rename(self.rawCsvFilePath, self.dataDirectory + '/' + self.rawCsvFile)


# Function called by csvProcess which does the actual data conversion on each data item
def convert(value, item):
    return value * conversion[item][0] + conversion[item][1]


# General init functions - including gain list setup and loading in program config
def init():
    # Create Dicts/Vars
    # Conversion contains m and c values used for converting raw data to real values
    global conversion
    conversion = {}

    # Allow user to Select Files - this creates an instance of the fileSelect class and runs the __init__ method
    global file
    file = fileSelect()
    # Start conversion process
    conversionSetup()
    csvProcess()


# Importing the information from the config file and creating a dictionary for m and c values needed for data conversion
def conversionSetup():
    # Load Config from File
    global config
    config = configparser.ConfigParser()
    config.read(file.configFilePath)
    # Process config for all enabled channels in config file
    for key in config.sections():
        if key != 'General' and config[key].getboolean('enabled') is True:
            # Get values of m and c (in y = mx + c) from config
            conversion[key] = (config[key].getfloat('m'), config[key].getfloat('c'))


# Loading CSV into pandas, processing the data and exporting converted CSV
def csvProcess():
    # Read CSV file
    df = pd.read_csv(file.rawCsvFilePath)
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
    df.to_csv(file.convertedCsvFilePath, sep=',', index=False)
    # Moving raw data and config into data folder with the converted csv
    file.fileCleanup()
    print("\nSuccess")


if __name__ == "__main__":
    init()
