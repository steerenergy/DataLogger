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
        # Pandas Dataframe
        self.df = None
        # Trigger Pandas Init
        self.pandasInit()

    # Initiate pandas and load CSV
    def pandasInit(self):
        # Load in CSV and print CSV contents
        self.df = pd.read_csv(self.convertedCsvFilePath)
        print("\nCurrent Data Preview:")
        # Printing top of the data
        print(self.df.head())
        # Converting the First Column to DateTime (Used for Compression)
        self.df.iloc[:, 0] = pd.to_datetime(self.df.iloc[:, 0])
        # Converting the Second Column to DateTime (Used for Compression)
        self.df.iloc[:, 1] = pd.to_datetime(self.df.iloc[:, 1])
        print(self.df)
        print("\n" + str(self.df.dtypes))
        # Set Index
        self.df.index = self.df.iloc[:, 0]

    # Filter Functions
    def filter(self):
        pass

    # Compress Functions
    def compress(self):
        print(self.df.iloc[:, 0])
        print(self.df.iloc[:, 0].resample('S'))

    # Plot Functions
    def plot(self):
        pass

    # Write Updated CSV File
    def pandasExit(self):
        print("\nWriting CSV...")
        # Write CSV
        self.df.to_csv(self.processedCsvFilePath, sep=',', index=False)
        print("\nSuccess")


# Main Menu
def init():
    # Create instance of process class
    data = Process()
    try:
        while True:
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
