# This uses tkinter which is a really common multi-platform GUI

import time
import threading
from tkinter import *
from tkinter import font
import logger
import sys


class WindowTop(Frame):
    # Main Window
    def __init__(self, master=None):
        # This is class inheritance
        Frame.__init__(self, master)
        # Setting self.master = master window
        self.master = master
        
        # Changing the title of our master widget
        self.master.title("Control:")
        self.pack()

        # Create Layout Frames
        self.topFrame = Frame(master)
        self.topFrame.pack(expand=1, fill=BOTH, side = LEFT)
        self.liveDataFrame = Frame(master)
        self.liveDataFrame.pack(expand=1,fill=BOTH, side = RIGHT)
        
        # Title
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
        liveDataScrollBar = Scrollbar(self.liveDataFrame)
        liveDataScrollBar.pack(side=RIGHT, fill=Y)

        # Live Data Text Box
        self.liveDataText = Text(self.liveDataFrame, yscrollcommand=liveDataScrollBar.set, font=smallFont ,state='disabled')
        self.liveDataText.pack()

        # Config ScrollBar
        liveDataScrollBar.config(command=self.liveDataText.yview)

    # The Button for Starting and Stopping Logging
    def logButtons(self):
        if self.logButton['text'] == "Start Logging":
            # Change Button Text
            self.logButton.config(text="Finish Logging")
            # Load Config Data and Setup
            logger.init()
            # Print Settings on Console
            logger.settingsOutput()
            # Run Logging
            logThread = threading.Thread(target=logger.log)
            logThread.start()
        else:
            print("Logging Finish")
            logger.logEnbl = False
            # Clear Text Output
            self.liveDataText['state'] = 'normal'
            self.liveDataText.delete(1.0, END)
            self.liveDataText['state'] = 'disabled'
            # Change Button Text
            self.logButton.config(text="Start Logging")

    # This redirects all print statements from console to the textbox.
    # It essentially replaces the print statement

    def redirector(self, inputStr):
        self.liveDataText['state'] = 'normal'
        self.liveDataText.insert(INSERT, inputStr)
        self.liveDataText['state'] = 'disabled'
        self.liveDataText.see("end")

    @staticmethod
    def client_exit():
        quit()


# Create Tkinter Instance
root = Tk()

# Size of the window (Uncomment for Full Scree)
# root.wm_attributes('-zoomed', 1)

# Fonts
bigFont = font.Font(family="Trebuchet MS", size=20, weight=font.BOLD)
smallFont = font.Font(family="Consolas", size=14)

app = WindowTop(root)

# Redirect all print statements to the textbox
sys.stdout.write = app.redirector

root.mainloop()
