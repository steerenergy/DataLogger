# This uses tkinter which is a really common multi-platform GUI
# Script connects to logger.py and acts a front end to it

import threading
from tkinter import *
from tkinter import font
import logger
import sys
import time


class WindowTop(Frame):
    # Main Window - Init function contains all elements of layout
    def __init__(self, master=None):
        # This is class inheritance
        Frame.__init__(self, master)
        # Setting self.master = master window
        self.master = master
        
        # Changing the title of our master widget
        self.master.title("Steer Energy Data Logger")
        self.pack()

        # Create Layout Frames
        self.topFrame = Frame(master)
        self.topFrame.pack(expand=1, fill=BOTH, side = LEFT)
        self.liveDataFrame = Frame(master)
        self.liveDataFrame.pack(expand=1, fill=BOTH, side=RIGHT)
        
        # Title text
        self.title = Label(self.topFrame, text="Log Ctrl:", font=bigFont)
        self.title.pack()

        # Start/Stop Logging Button 
        self.logButton = Button(self.topFrame, text="Start Logging", height=3, width=20, command=self.logButtons, font=bigFont)
        self.logButton.pack()

        # Start/Stop Logging Button
        self.quitButton = Button(self.topFrame, text="Quit", height=3, width=20, command=self.client_exit, font=bigFont)
        self.quitButton.pack(padx=10)

        # Live Data Title
        self.liveTitle = Label(self.liveDataFrame, text="Live Data:", font=bigFont)
        self.liveTitle.pack(side=TOP)

        # Live Data Scroll Bar
        self.liveDataScrollBar = Scrollbar(self.liveDataFrame)
        self.liveDataScrollBar.pack(side=RIGHT, fill=Y)

        # Live Data Text Box
        self.liveDataText = Text(self.liveDataFrame, yscrollcommand=self.liveDataScrollBar.set, font=smallFont, state='disabled')
        self.liveDataText.pack()

        # Config ScrollBar
        self.liveDataScrollBar.config(command=self.liveDataText.yview)

        # Checkbox for AutoScroll
        self.autoScrollEnable = IntVar()
        self.autoScroll = Checkbutton(self.topFrame, text="AutoScroll", variable=self.autoScrollEnable, font=bigFont)
        self.autoScroll.select()
        self.autoScroll.pack()

        # Redirect normal print commands to textbox on GUI
        sys.stdout.write = self.redirector

        # Holds the number of lines in the textbox (updated after each print)
        self.textIndex = None
        # Determines the max number of lines on the tkinter GUI at any given point.
        self.textThreshold = 250.

        # The scripts for starting and stopping logging
    def logButtons(self):
        # Starting Logging
        if self.logButton['text'] == "Start Logging":
            # Disable Log Button
            self.logButton['state'] = 'disabled'
            # Clear Text Output
            self.liveDataText['state'] = 'normal'
            self.liveDataText.delete(1.0, END)
            self.liveDataText['state'] = 'disabled'
            # Scroll to Bottom of Blank Box
            self.liveDataText.see(END)
            # Load Config Data and Setup
            logger.init()
            # Print Settings on Console
            logger.settingsOutput()
            # Run Logging
            self.logThread = threading.Thread(target=logger.log)
            self.logThread.start()
            # Change Button Text and re-enable
            self.logButton.config(text="Finish Logging")
            self.logButton['state'] = 'normal'
        # Stopping Logging
        else:
            # Disable button
            self.logButton['state'] = 'disabled'
            # Print button status
            print("\nStopping Logger... ", end="", flush=True)
            logger.logEnbl = False
            # Wait until logger thread is finished - delay put in to stop crash of program when start/stop is too quick
            time.sleep(0.1)
            self.logThread.join()
            print("Success!")
            # Change Button Text
            self.logButton.config(text="Start Logging")
            # Re-enable Button
            self.logButton['state'] = 'normal'

    # This redirects all print statements from console to the textbox in the GUI.
    # Note - errors will be displayed in terminal still
    # It essentially redefines what the print statement does
    def redirector(self, inputStr):
        # Enable, write data, delete unecessary data, disable
        self.liveDataText['state'] = 'normal'
        self.liveDataText.insert(END, inputStr)
        # If over a certain amount of lines, delete all lines from the top up to a threshold
        self.textIndex = float(self.liveDataText.index('end'))
        if self.textIndex > self.textThreshold:
            self.liveDataText.delete(1.0, self.textIndex-self.textThreshold)
        # If autoscroll is enabled, then scroll to bottom
        self.liveDataText.update()
        self.liveDataText['state'] = 'disabled'
        if self.autoScrollEnable.get() == 1:
            self.liveDataText.see(END)

    @staticmethod
    def client_exit():
        quit()


# Create Tkinter Instance
root = Tk()

# Size of the window (Uncomment for Full Screen)
# root.wm_attributes('-zoomed', 1)

# Fonts
bigFont = font.Font(family="Helvetica", size=20, weight=font.BOLD)
smallFont = font.Font(family="Courier", size=14)

app = WindowTop(root)

root.mainloop()
