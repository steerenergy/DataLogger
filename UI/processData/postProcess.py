# Column references should always be done numerically
# Each function must reset it's index once finished (if an index is set)

# General Imports
import common
import os
import time
# Pandas Import Statements - Once completed unused ones can be removed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# Contains all the functions for processing data and loading/exporting the CSV file
# def defines the methods in the class 'Process' these are functions in the class
class Process:
    def __init__(self):
        # File Selection variable
        self.valid = True
        # File Holding Variables
        self.csvList = []
        self.csvDirectory = "files/converted"
        self.csvDirContents = os.listdir(self.csvDirectory)
        self.convertedCsvFile = None
        self.convertedCsvFilePath = None
        self.processedCsvFile = None
        self.processedCsvFilePath = None

        # Pandas DataFrame
        self.df = None
        # Hold Pandas DF graph
        self.ax = None

        # Graph Settings
        self.yData = {}
        self.xData = None
        self.plotTitle = "Plot"
        self.plotYTitle = "Values"

        # Begin File Selection
        self.fileSelect()

        # Trigger Pandas Init if self.valid is true (file correctly selected)
        if self.valid is True:
            self.pandasInit()

    def fileSelect(self):
        # Create list of CSV files with 'converted' in name
        self.csvList = [fileName for fileName in self.csvDirContents
                        if fileName.endswith('.csv') and fileName.startswith('converted')]

        # Dealing with cases where there are no matching files in directory
        if len(self.csvList) <= 0:
            print("\nNo Data Found - Please ensure there is at least 1 'convertedXXX.csv' file in the folder")
            # Setting the var false makes the self.fileSelect function not run and stops the program
            self.valid = False
        else:
            try:
                # Data Selection
                print("\nData Found - Current Files:")
                # Counter used for options
                # Print Output in nice format
                for pos, fileName in enumerate(self.csvList, start=1):
                    print("{}. {}".format(pos, fileName))
                # User Selection
                option = int(input("Please select a file (by its corresponding number):  "))
                # If number valid on list, choose that CSV file
                if 0 < option <= len(self.csvList):
                    # Set filepath to open and with it the filepath/directories for processed data
                    self.convertedCsvFile = self.csvList[option-1]
                    self.convertedCsvFilePath = self.csvDirectory + "/" + self.convertedCsvFile
                    self.processedCsvFile = self.convertedCsvFile.replace("converted", "processed")
                    self.processedCsvFilePath = self.csvDirectory + "/" + self.processedCsvFile
                # If a number is typed in out of range
                else:
                    common.other()
                    self.valid = False
            # If a user doesn't type in an integer
            except ValueError:
                common.other()
                self.valid = False

    # Create pandas DataFrame object (df) and load CSV
    def pandasInit(self):
        print("\nLoading CSV File...")
        # Load in CSV and print CSV contents
        self.df = pd.read_csv(self.convertedCsvFilePath)
        # Converting the First Column to DateTime (Used for Compression)
        self.df.iloc[:, 0] = pd.to_datetime(self.df.iloc[:, 0])
        # Converting the Second Column to TimeDelta (Used for Compression)
        self.df.iloc[:, 1] = pd.to_timedelta(self.df.iloc[:, 1], unit='s')
        # Add columns to yData dict for plot selection and set all to true by default beyond the first two time columns
        for column in self.df.columns:
            if column in self.df.columns[2:]:
                self.yData[column] = True
            else:
                self.yData[column] = False
        # Set default x column for plotting
        self.xData = self.df.columns[0]
        print("Success!")

    # Current Data Output
    def currentData(self):
        # Short Delay to stop your head going blurry
        time.sleep(0.5)
        # Printing top of the data
        print("\nCurrent Data Preview:")
        print(self.df.head())
        # Printing Data Types
        print("\nCurrent Data Types (Excl Selected Index):")
        print("\n" + str(self.df.dtypes))

    # Filter Functions
    def filter(self):
        # Print that we are in the filter function
        print("\n In the Filter Option")
        # Rolling is the pandas moving average function

        # self is re-writing itself iloc is a pandas function to reference the array
        self.df.iloc[:, 2] = self.df.iloc[:, 2].rolling(4).sum()

    # Compress Functions (using Pandas Resample Func)
    def compress(self):
        try:
            # Find out what user wants the compression time
            num = float(input("Type in the new logging interval desired in Seconds: "))

            # Set Index to column with time interval (By getting heading name of second column in process)
            self.df.set_index(self.df.columns[1], inplace=True)
            # Resample Date/Time, then the rest. Do this on two separate dataframes
            dfComp1 = self.df.iloc[:, 0].resample(str(num)+'S').first()
            # Change '.mean' to whatever function you wish from the following URL:
            # (http://pandas.pydata.org/pandas-docs/stable/groupby.html#groupby-dispatch)
            dfComp2 = self.df.iloc[:, 1:].resample(str(num) + 'S').mean()

            # Combine the dataframes and set equal to the original one
            self.df = pd.concat([dfComp1, dfComp2], axis=1)
            # Remove Index
            self.df.reset_index(inplace=True)

            # Reset Column Positioning (move Time-Interval back to position 2)
            cols = list(self.df.columns.values)
            cols[0], cols[1] = cols[1], cols[0]
            self.df = self.df[cols]
        except ValueError:
            common.other()

    # Plot Functions
    def plotSettings(self):
        # Menu for selecting options for user to choose what the grap1h Looks Like
        try:
            while True:
                # Print options and current settings
                option = input("\nPlot Options - Current Settings: \nChoose a Option to change a setting"
                               " (based on the corresponding number): "
                               "\n1. Select Data\n2. Plot Title: '{}'\n3. Y Axis Title: '{}'\n4. Plot"
                               "\n----------------\n5. Back\n\nOption Chosen: "
                               .format(self.plotTitle, self.plotYTitle))
                if option == "1":
                    self.plotSelectData()
                elif option == "2":
                    # Change Title of Graph
                    self.plotTitle = input("\nInput the Graph Title: ")
                elif option == "3":
                    # Change Y axis Title
                    self.plotYTitle = input("\nInput the Y Axis Title: ")
                elif option == "4":
                    self.plotGraph()
                elif option == "5":
                    common.back()
                else:
                    common.other()
        except StopIteration:
            pass

    # Select for the Y and X Axis
    def plotSelectData(self):
        # Choose Y axis Data
        try:
            while True:
                print("\nY Axis: Columns Selected for Plotting ")
                # Counter used for options
                x = 1
                # Print Output in nice format
                for item in self.yData:
                    print("{}. {:>24} : {}".format(x, item, self.yData[item]))
                    x += 1
                print("{} \n{}. Save/Next".format("-"*35, x))
                # User Selection
                option = int(input("Choose a number to toggle selection: "))
                # If number is in list index
                if 0 < option <= len(self.yData):
                    # Get name of column and toggle visablity on graph
                    colName = self.df.columns[option - 1]
                    self.yData[colName] = not self.yData[colName]
                # Go back, if back option is selected
                elif option == x:
                    common.back()
                # If a number is typed in out of range
                else:
                    common.other()
        except StopIteration:
            pass
        # If someone does not put in an integer
        except ValueError:
            common.other()

        # X Axis Selection
        try:
            while True:
                print("\nX Axis: Currently Selected: {} ".format(self.xData))
                # Counter used for options
                x = 1
                # Print Output in nice format
                for item in self.yData:
                    print("{}. {}".format(x, item))
                    x += 1
                print("{} \n{}. Save/Next".format("-"*30, x))
                # User Selection
                option = int(input("Choose a number to select column: "))
                # If valid number on the list then toggle it
                # Get name of column
                if 0 < option <= len(self.yData):
                    colName = self.df.columns[option - 1]
                    self.xData = colName
                # Go back, if back option is selected
                elif option == x:
                    common.back()
                # If a number is typed in out of range
                else:
                    common.other()
        except StopIteration:
            pass
        # If someone does not put in an integer
        except ValueError:
            common.other()

    def plotGraph(self):
        # Create list of columns to be plotted on y axis (using list comprehension)
        yColumns = [column for column in self.yData if self.yData[column] is True]
        # Convert time to numeric for plotting
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1].dt.total_seconds())
        # Create graph with x,y and user title chosen
        self.ax = self.df.plot(x=self.xData, y=yColumns, title=self.plotTitle)
        # Set Y axis Label (X axis is already set by default as column heading)
        self.ax.set(ylabel=self.plotYTitle)
        # Turn on minor ticks on Graph for better reading
        plt.minorticks_on()
        # Warn User to Close Windows to Continue
        print("Opening Plot... Please close the graph window to continue")
        # Show the graph
        plt.show()
        # Convert time back to timedelta
        self.df.iloc[:, 1] = pd.to_timedelta(self.df.iloc[:, 1], unit='s')

    # Write Updated CSV File
    def pandasExit(self):
        # Write CSV
        print("\nWriting CSV...")
        # Convert time interval back to a float - ensuring it is in seconds
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1].dt.total_seconds())
        # Write CSV
        self.df.to_csv(self.processedCsvFilePath, sep=',', index=False)
        # Reset time interval as before
        self.df.iloc[:, 1] = pd.to_timedelta(self.df.iloc[:, 1], unit='s')
        print("\nSuccess")


# Main PostProcess Menu
def init():
    # Create instance of process class
    data = Process()
    # Only continue if valid data has been selected
    if data.valid is True:
        try:
            while True:
                # Print Current Data
                data.currentData()
                option = input("\nPost Process Menu: \nChoose a Option (based on the corresponding number): "
                               "\n1. Filter\n2. Compress\n3. Plot\n4. Save File"
                               "\n----------------\n5. Back\n\nOption Chosen: ")
                if option == "1":
                    data.filter()
                elif option == "2":
                    data.compress()
                elif option == "3":
                    data.plotSettings()
                elif option == "4":
                    data.pandasExit()
                elif option == "5":
                    common.back()
                else:
                    common.other()
        except StopIteration:
            pass
