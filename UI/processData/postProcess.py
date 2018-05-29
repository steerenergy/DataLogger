# General Imports
import common
# Pandas Import Statements - Once completed unused ones can be removed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csvFilePath = "/files/converted/"


# Main Menu
def init():
    try:
        while True:
            option = input("\nPost Process Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Filter\n2. Compress\n3. Plot"
                           "\n4. Back\n5. Quit \n\nOption Chosen: ")
            if option == "1":
                dataFilter()
            elif option == "2":
                dataCompress()
            elif option == "3":
                dataPlot()
            elif option == "4":
                common.back()
            elif option == "5":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass


# Filter Functions
def dataFilter():
    pass


# Compress Functions
def dataCompress():
    pass


# Plot Functions
def dataPlot():
    pass
