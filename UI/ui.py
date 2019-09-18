# MAIN PROGRAM - Run this!

# Hide Matplotlib depreciation warning - temporary fix until pyisntaller updates
# Check https://github.com/pyinstaller/pyinstaller/issues/3959 for more
import warnings
warnings.filterwarnings('ignore')
# Import menu (which with it imports all other modules)
import menu

# Initiate Main Menu
menu.init()
