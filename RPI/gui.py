# This uses tkinter which is a really common multi-platform GUI

import threading
from tkinter import *
from tkinter import font
import logger


class Window(Frame):
    # Main Window
    def __init__(self, master=None):
        # This is class inheritance
        Frame.__init__(self, master)
        # Setting self.master = master window
        self.master = master

        # Changing the title of our master widget
        self.master.title("Data Logger")
        self.pack()

        # Title
        self.label = Label(self, text="Data Logger", font=chosenFont)
        self.label.pack()

        # Start/Stop Logging Button 
        self.logButton = Button(text="Start Logging", height=4, width=20, command=self.test, font=chosenFont)
        self.logButton.pack(side=TOP)

        # Start/Stop Logging Button 
        self.quitButton = Button(text="Quit", height=4, width=20, command=self.client_exit, font=chosenFont)
        self.quitButton.pack(side=BOTTOM)

    def test(self):
        if self.logButton['text'] == "Start Logging":
            print("Logging Start")
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
chosenFont = font.Font(family="Helvetica", size=20, weight=font.BOLD)

app = Window(root)
root.mainloop()
