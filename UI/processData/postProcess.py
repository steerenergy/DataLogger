# General Imports
import common
# Pandas Import Statements - Once completed unused ones can be removed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Contains all the functions for processing data and loading/exporting the CSV file
class Process:
    def __init__(self):
        # This is a temporary file path. A file selection system will need to be implemented (See X01 doc)
        self.csvDirectory = "files/converted"
        self.convertedCsvFile = "converted20180529170314.311127.csv"
        self.convertedCsvFilePath = self.csvDirectory + "/" + self.convertedCsvFile
        self.processedCsvFile = self.convertedCsvFile.replace("converted", "processed")
        self.processedCsvFilePath = self.csvDirectory + "/" + self.processedCsvFile
        # Pandas DataFrame
        self.df = None
        # Trigger Pandas Init
        self.pandasInit()

    # Initiate pandas and load CSV
    def pandasInit(self):
        # Load in CSV and print CSV contents
        self.df = pd.read_csv(self.convertedCsvFilePath)
        # Set Index
        self.df.set_index('Date/Time', inplace=True)
        # Converting the First Column to DateTime (Used for Compression)
        self.df.index = pd.to_datetime(self.df.index)
        # Converting the Second Column to DateTime (Used for Compression)
        self.df.iloc[:, 0] = pd.to_timedelta(self.df.iloc[:, 0], unit='s')
        # Printing Data Types
        print("\n" + str(self.df.dtypes))

    # Current Data Output
    def currentData(self):
        # Printing top of the data
        print("\nCurrent Data Preview:")
        print(self.df.head())

    # Filter Functions
    def filter(self):
        pass

    # Compress Functions
    def compress(self):
        # print(self.df.iloc[:, 0])
        print("\nCOMPRESSION\n")
        self.df = self.df.iloc[:, 1:].resample('T').mean()
        # self.df = self.df.resample('T').mean()

    # Plot Functions
    def plot(self):
        pass

    # Write Updated CSV File
    def pandasExit(self):
        print("\nWriting CSV...")
        # Write CSV
        self.df.to_csv(self.processedCsvFilePath, sep=',', index=True)
        print("\nSuccess")


# Main Menu
def init():
    # Create instance of process class
    data = Process()
    try:
        while True:
            # Print Current Data
            data.currentData()
            option = input("\nPost Process Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Filter\n2. Compress\n3. Plot\n4. Save File"
                           "\n----------------\n5. Back\n6. Quit \n\nOption Chosen: ")
            if option == "1":
                data.filter()
            elif option == "2":
                data.compress()
            elif option == "3":
                data.plot()
            elif option == "4":
                data.pandasExit()
            elif option == "5":
                common.back()
            elif option == "6":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass
