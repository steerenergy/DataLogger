# General Imports
import common
# Pandas Import Statements - Once completed unused ones can be removed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Process:
    def __init__(self):
        # This is a temporary file path. A file selection system will need to be implemented (See X01 doc)
        self.csvFilePath = "files/converted/raw20180525120257197352.csv"
        self.df = None
        # Trigger Pandas Init
        self.pandasInit()

    def pandasInit(self):
        self.df = pd.read_csv(self.csvFilePath)
        print("\nCurrent Data:")
        print(self.df.head)

    # Filter Functions
    def filter(self):
        pass

    # Compress Functions
    def compress(self):
        pass

    # Plot Functions
    def plot(self):
        pass


# Main Menu
def init():
    # Create instance of process class
    data = Process()
    try:
        while True:
            option = input("\nPost Process Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Filter\n2. Compress\n3. Plot"
                           "\n4. Back\n5. Quit \n\nOption Chosen: ")
            if option == "1":
                data.filter()
            elif option == "2":
                data.compress()
            elif option == "3":
                data.plot()
            elif option == "4":
                common.back()
            elif option == "5":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass
