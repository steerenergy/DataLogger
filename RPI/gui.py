# This uses tkinter which is a really common multi-platform GUI

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
        self.master.title("Data Logger")
        self.pack()

        # Create Layout Frames
        self.topFrame = Frame(master)
        self.topFrame.pack(expand=1, fill=BOTH)
        self.liveData = Frame(master, bg="red")
        self.liveData.pack(expand=1,fill=BOTH)
        
        # Title
        self.title = Label(self.topFrame, text="Data Logger", font=bigFont)
        self.title.pack()

        # Start/Stop Logging Button 
        self.logButton = Button(self.topFrame, text="Start Logging", height=4, width=20, command=self.logButtons, font=bigFont)
        self.logButton.pack()

        # Start/Stop Logging Button 
        self.quitButton = Button(self.topFrame, text="Quit", height=4, width=20, command=self.client_exit, font=bigFont)
        self.quitButton.pack()

        # Live Data Title
        self.liveTitle = Label(self.liveData, text="Live Data:", font=smallFont)
        self.liveTitle.pack()

        #Live Data Table
        #TBD

    def logButtons(self):
        if self.logButton['text'] == "Start Logging":
            # Change Button Text
            self.logButton.config(text="Finish Logging")
            # Load Config Data and Setup
            logger.init()
            # Print Settings
            logger.settingsOutput()
            # Run Logging
            logThread = threading.Thread(target=logger.log)
            logThread.start()
        else:
            print("Logging Finish")
            logger.logEnbl = False
            # Change Button Text
            self.logButton.config(text="Start Logging")

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
