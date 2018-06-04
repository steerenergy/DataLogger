# Column references should always be done numerically
# Each function must reset it's index once finished (if an index is set)

# General Imports
import common
import time
# Pandas Import Statements - Once completed unused ones can be removed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


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
        # Hold Pandas DF graph
        self.ax = None

        # Graph Settings
        self.yData = {}
        self.plotTitle = "Plot"
        self.plotYTitle = "Values"

        # Trigger Pandas Init
        self.pandasInit()

        # Initiate Pandas and load CSV
    def pandasInit(self):
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
        pass

    # Compress Functions (using Pandas Resample Func)
    def compress(self):
        try:
            # Find out what user wants the compression time
            num = float(input("Type in the new logging interval desired in Seconds: "))

            # Set Index to column with time interval (By getting heading name of second column in process)
            self.df.set_index(self.df.columns[1], inplace=True)
            # Resample Date/Time, then the rest. Do this on two separate dataframes
            dfComp1 = self.df[self.df.columns[0]].resample(str(num)+'S').first()
            # Change '.mean' to whatever function you wish from the following URL:
            # (http://pandas.pydata.org/pandas-docs/stable/groupby.html#groupby-dispatch)
            dfComp2 = self.df[self.df.columns[1:]].resample(str(num) + 'S').mean()

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
                               "(based on the corresponding number): "
                               "\n1. Data Selected: {}\n2. Plot Title: {}\n3. Y Axis Title: {}\n4. Plot"
                               "\n----------------\n5. Back\n6. Quit \n\nOption Chosen: "
                               .format("placeholder 1", self.plotTitle, self.plotYTitle))
                if option == "1":
                    self.plotSelectData()
                elif option == "2":
                    # Change Title of Graph
                    self.plotTitle = input("\nInput the Graph Title: ")
                elif option == "3":
                    # Change Y axis Title
                    self.plotYTitle = input("\nInput the Graph Title: ")
                elif option == "4":
                    self.plotGraph()
                elif option == "5":
                    common.back()
                elif option == "6":
                    common.quit()
                else:
                    common.other()
        except StopIteration:
            pass

    def plotSelectData(self):
        try:
            while True:
                print("Y Axis: Columns Selected for Plotting ")
                # Counter used for options
                x = 1
                # Print Output in nice format
                for item in self.yData:
                    print("{}. {:>24} : {}".format(x, item, self.yData[item]))
                    x += 1
                print("{} \n{}. Save/Back".format("-"*30,x))
                # User Selection
                option = input("Choose a number to toggle: ")
                # If valid number on the list then toggle it
                # Get name of column
                if 0 < int(option) <= len(self.yData):
                    colName = self.df.columns[int(option) - 1]
                    self.yData[colName] = not self.yData[colName]
                # Go back if back option selected
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
        #
        # --
        # Print All Columns and selection status
        # User Selects each column they want to be enabled until they choose 'save'
        # Selected columns added to list of columns to be plotted

        # TO DEVELOP

    def plotGraph(self):
        # Convert time to numeric for plotting
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1])
        self.ax = self.df.plot(x=self.df.columns[1], y=self.df.columns[2:], title=self.plotTitle)
        # Set Y axis Label (X axis is already set by default as column heading)
        self.ax.set(ylabel=self.plotYTitle)
        # Turn on Minor Ticks on Graph for better reading
        plt.minorticks_on()
        # Show the graph
        plt.show()
        # Convert time back to timedelta
        self.df.iloc[:, 1] = pd.to_timedelta(self.df.iloc[:, 1])

    # Write Updated CSV File
    def pandasExit(self):
        print("\nWriting CSV...")
        # Convert time interval back to previous format
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1])
        # Write CSV
        self.df.to_csv(self.processedCsvFilePath, sep=',', index=False)
        # Reset time interval as before
        self.df.iloc[:, 1] = pd.to_timedelta(self.df.iloc[:, 1], unit='s')
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
                data.plotSettings()
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
