# General Imports
import common


# Main Menu
def init():
    try:
        while True:
            option = input("\nPost Process Menu: \nChoose a Option (based on the corresponding number): "
                           "\n1. Filter\n2. Compress\n3. Plot"
                           "\n4. Back\n5. Quit \n\nOption Chosen: ")
            if option == "1":
                filter()
            elif option == "2":
                compress()
            elif option == "3":
                plot()
            elif option == "4":
                common.back()
            elif option == "5":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass


# Filter Functions
def filter():
    pass


# Compress Functions
def compress():
    pass


# Plot Functions
def plot():
    pass