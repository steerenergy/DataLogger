# This uses tkinter which is a really common multi-platform GUI

import time
import threading
from tkinter import *
from tkinter import font
import logger


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

        # Live Data Text Box
        self.liveDataText = Text(self.liveDataFrame,font=smallFont)
        self.liveDataText.pack()

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
            # Start Live Data
            dataThread = threading.Thread(target=self.liveData)
            dataThread.start()
        else:
            print("Logging Finish")
            logger.logEnbl = False
            # Change Button Text
            self.logButton.config(text="Start Logging")

    def liveData(self):
        # Setup data buffer to hold most recent data
        buffer = 0
        while logger.logEnbl is True:
            # Get Complete Set of Logged Data
            # If Data is different to that in the buffer
            if logger.adcValuesCompl != buffer:
                buffer = logger.adcValuesCompl
                self.liveDataText.insert(END,"{}\n".format(buffer))
                self.liveDataText.pack()
            # Sleep - Don't want to go too fast
            time.sleep(0.05)
    
    @staticmethod
    def client_exit():
        quit()


# Create Tkinter Instance
root = Tk()

# Size of the window
# root.wm_attributes('-zoomed', 1)

# Fonts
bigFont = font.Font(family="Helvetica", size=20, weight=font.BOLD)
smallFont = font.Font(family="Helvetica", size=14)

app = WindowTop(root)
root.mainloop()
