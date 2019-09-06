# PostProcess is responsible for processing converted data to make it more useful
# Program begins at init, creating an instance of the Process class
# This triggers fileSelect for user file selection and then pandasInit which loads in the CSV into a pandas dataframe
# Then the ini function creates a menu with a list of functions. Each function links to one of the Process' methods
# Some options can be customised by the menus but many more can be done by editing this code. Follow the comments
# Definitely check out '10 minutes to pandas' - give it a quick google search

# IMPORTANT RULES when writing or modifying functions:
# Column references should always be done numerically (using 'iloc' or 'self.df.columns' where necessary)
# Each function must reset it's index once finished (if an index is set) and put it back into the right conditions

# General Imports
import common
import os
import time
# Pandas Import Statements
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# Contains all the functions for processing data and loading/exporting the CSV file
# def defines the methods in the class 'Process' these are functions in the class
class Process:
    # Class Constructor
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
        self.ax2 = None

        # Graph Settings
        self.yDataPrimary = {}
        self.yDataSecondary = {}
        self.xData = None
        self.plotTitle = "Plot"
        self.plotYPrimaryTitle = "Values"
        self.plotYSecondaryTitle = "Values"

        # Begin File Selection
        self.fileSelect()

        # Trigger Pandas Init if self.valid is true (file correctly selected)
        if self.valid is True:
            self.pandasInit()

    # User File Selection
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
                # Data Selection List
                print("\nData Found - Current Files:")
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
                self.yDataPrimary[column] = True
            else:
                self.yDataPrimary[column] = False
            # By Default, Secondary Axis is turned off
            self.yDataSecondary[column] = False
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
        print(str(self.df.dtypes) + "\n")

    # Filter Functions
    def filter(self):
        # NICK RYA - WORK IN PROGRESS
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
                               "\n1. Select Data\n2. Plot Title: '{}'\n3. Primary Y Axis Title: '{}'"
                               "\n4. Secondary Y Axis Title: '{}'\n5. Plot "
                               "\n----------------\n6. Back\n\nOption Chosen: "
                               .format(self.plotTitle, self.plotYPrimaryTitle, self.plotYSecondaryTitle))
                if option == "1":
                    self.plotSelectData()
                elif option == "2":
                    # Change Title of Graph
                    self.plotTitle = input("\nInput the Graph Title: ")
                elif option == "3":
                    # Change Primary Y Axis Title
                    self.plotYPrimaryTitle = input("\nInput the Primary Y Axis Title: ")
                elif option == "4":
                    # Change Secondary Y Axis Title
                    self.plotYSecondaryTitle = input("\nInput the Secondary Y Axis Title: ")

                elif option == "5":
                    self.plotGraph()
                elif option == "6":
                    common.back()
                else:
                    common.other()
        except StopIteration:
            pass

    # Select for the Y and X Axis
    def plotSelectData(self):
        # Choose Primary Y axis Data
        try:
            while True:
                print("\nPrimary Y Axis: Columns Selected for Plotting ")
                # Counter used for options
                x = 1
                # Print Output in nice format
                for item in self.yDataPrimary:
                    print("{}. {:>24} : {}".format(x, item, self.yDataPrimary[item]))
                    x += 1
                print("{} \n{}. Save/Next".format("-"*35, x))
                # User Selection
                option = int(input("Choose a number to toggle selection: "))
                # If number is in list index
                if 0 < option <= len(self.yDataPrimary):
                    # Get name of column and toggle visibility on graph
                    colName = self.df.columns[option - 1]
                    self.yDataPrimary[colName] = not self.yDataPrimary[colName]
                # End loop if next option is selected
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

        # Choose Secondary Y axis Data
        try:
            while True:
                print("\nSecondary Y Axis: Columns Selected for Plotting ")
                # Counter used for options
                x = 1
                # Print Output in nice format
                for item in self.yDataSecondary:
                    print("{}. {:>24} : {}".format(x, item, self.yDataSecondary[item]))
                    x += 1
                print("{} \n{}. Save/Next".format("-" * 35, x))
                # User Selection
                option = int(input("Choose a number to toggle selection: "))
                # If number is in list index
                if 0 < option <= len(self.yDataSecondary):
                    # Get name of column and toggle visibility on graph
                    colName = self.df.columns[option - 1]
                    self.yDataSecondary[colName] = not self.yDataSecondary[colName]
                # End loop if next option is selected
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
                for item in self.yDataPrimary:
                    print("{}. {}".format(x, item))
                    x += 1
                print("{} \n{}. Save/Next".format("-"*30, x))
                # User Selection
                option = int(input("Choose a number to select column: "))
                # If valid number on the list then toggle it
                # Get name of column
                if 0 < option <= len(self.yDataPrimary):
                    colName = self.df.columns[option - 1]
                    self.xData = colName
                # End loop if next option is selected
                elif option == x:
                    print("Success! - Plot Settings Updated")
                    common.back()
                # If a number is typed in out of range
                else:
                    common.other()
        except StopIteration:
            pass
        # If someone does not put in an integer
        except ValueError:
            common.other()

    # Graph Plotting Functions
    def plotGraph(self):
        # Create list of primary columns in csv to be plotted on y axis (using list comprehension)
        yColumnsPrimary = [column for column in self.yDataPrimary if self.yDataPrimary[column] is True]
        # Create list of secondary columns in csv to be plotted on y axis (using list comprehension)
        yColumnsSecondary = [column for column in self.yDataSecondary if self.yDataSecondary[column] is True]
        # Convert time to numeric for plotting
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1].dt.total_seconds())
        # Create graph with x,y and user title chosen
        self.ax = self.df.plot(x=self.xData, y=yColumnsPrimary, title=self.plotTitle)
        # Set Primary Y Axis Label (X axis is already set by default as column heading)
        self.ax.set_ylabel(self.plotYPrimaryTitle)
        # Set Primary Legend Location
        self.ax.legend(loc='upper left')
        # Set Grid Lines (Major and Minor)
        self.ax.grid(which="major", axis="both", color="black", linestyle="-", alpha=2, linewidth=.3)
        self.ax.grid(which="minor", axis="both", color="black", linestyle=":", alpha=10, linewidth=.15)
        # Set Plot Background
        self.ax.set_facecolor('white')
        # Set Spines (Borders) for each side
        for side in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[side].set_color('black')

        # Plot secondary axis only if it isn't empty
        if len(yColumnsSecondary) > 0:
            # Set Twin Axis
            self.ax2 = self.ax.twinx()
            # Set the colour cycle of the 2nd axis to the first
            # It automatically takes the next colour after the previous on the primary Y axis
            self.ax2._get_lines.prop_cycler = self.ax._get_lines.prop_cycler
            # Plot 2nd axis
            self.df.plot(x=self.xData, y=yColumnsSecondary, ax=self.ax2)
            # Set Secondary Y Axis Label
            self.ax2.set_ylabel(self.plotYSecondaryTitle, rotation=270, va='bottom')
            # Set Secondary Legend Location
            self.ax2.legend(loc='upper right')
            # Turn off grid (horizontal lines between ticks)
            self.ax2.grid(None)
        # Turn on minor ticks on Graph for better reading
        plt.minorticks_on()
        # Warn User to Close Windows to Continue
        print("Opening Plot... Please close the graph window to continue."
              "\nIf the window is closed and the program has not continued after several seconds, press any key'")
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
                               "\n1. Filter (Work in Progress)\n2. Compress\n3. Plot\n4. Save File"
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
