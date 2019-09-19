# This uses tkinter which is a really common multi-platform GUI
# Script connects to logger.py and acts a front end to it

import logging
from datetime import datetime
import threading
from tkinter import *
from tkinter import font, messagebox
import logger
import sys


class WindowTop(Frame):
    # Main Window - Init function contains all elements of layout
    def __init__(self, master=None):
        # This is class inheritance
        Frame.__init__(self, master)
        # Setting self.master = master window
        self.master = master

        # Changing the title of our master widget
        self.master.title("Steer Energy Data Logger V1.1.3")
        self.pack()

        # Create Layout Frames
        self.topFrame = Frame(master)
        self.topFrame.pack(expand=1, fill=BOTH, side=LEFT)
        self.liveDataFrame = Frame(master)
        self.liveDataFrame.pack(expand=1, fill=BOTH, side=RIGHT)

        # Title Text
        self.title = Label(self.topFrame, text="Log Ctrl:", font=bigFont)
        self.title.pack()

        # Start/Stop Logging Button
        self.logButton = Button(self.topFrame, text="Start Logging", height=3, width=11, command=self.logToggle,
                                font=bigFont)
        self.logButton.pack(padx=5)

        # Quit Button
        self.quitButton = Button(self.topFrame, text="Quit", height=3, width=11, command=self.onClose, font=bigFont)
        self.quitButton.pack(padx=5)

        # Live Data Title
        self.liveTitle = Label(self.liveDataFrame, text="Live Data:", font=bigFont)
        self.liveTitle.pack(side=TOP)

        # Live Data Scroll Bar
        self.liveDataScrollBar = Scrollbar(self.liveDataFrame)
        self.liveDataScrollBar.pack(side=RIGHT, fill=Y)

        # Live Data Text Box
        self.liveDataText = Text(self.liveDataFrame, width=68, yscrollcommand=self.liveDataScrollBar.set,
                                 font=smallFont, state='disabled')
        self.liveDataText.pack()

        # Config ScrollBar
        self.liveDataScrollBar.config(command=self.liveDataText.yview)

        # Checkbox for AutoScroll
        self.autoScrollEnable = IntVar()
        self.autoScroll = Checkbutton(self.topFrame, text="AutoScroll", variable=self.autoScrollEnable, font=bigFont)
        self.autoScroll.select()
        self.autoScroll.pack(side=BOTTOM)

        # Redirect normal print commands to textbox on GUI
        sys.stdout.write = self.redirector

        # Holds the number of lines in the textbox (updated after each print)
        self.textIndex = None
        # Determines the max number of lines on the tkinter GUI at any given point.
        self.textThreshold = 250

        # Will later hold logThread
        self.logThread = None

    # Contains functions for the start/stop logging buttons
    def logToggle(self):
        # Starting Logging
        if self.logButton['text'] == "Start Logging":
            # Disable Log Button
            self.logButton['state'] = 'disabled'
            # Update button.
            # We need the change to happen now, rather than at the end of the function (in root.mainloop)
            self.logButton.update()
            # Clear Text Output
            self.liveDataText['state'] = 'normal'
            self.liveDataText.delete(1.0, END)
            # Remove history from RAM (to avoid memory leak)
            self.liveDataText.edit_reset()
            self.liveDataText['state'] = 'disabled'
            # Scroll to Bottom of Blank Box
            self.liveDataText.see(END)
            # Load and Start Logger thread
            self.logThread = threading.Thread(target=logger.run)
            self.logThread.start()
            # Change Button Text and re-enable
            self.logButton.config(text="Finish Logging")
            self.logButton['state'] = 'normal'
        # Stopping Logging
        else:
            # Disable button
            self.logButton['state'] = 'disabled'
            # Print button status
            print("\nStopping Logger")
            # Change logEnbl variable to false which stops the loop in logThread and subsequently the live data
            logger.logEnbl = False
            # Check to see if logThread has ended
            self.logThreadStopCheck()

    # Is triggered when 'Stop Logging' ic clicked and is called until logThread is dead
    # If logThread has finished the 'start logging' button is changed and enabled
    # Else, the function is triggered again after a certain period of time
    def logThreadStopCheck(self):
        if self.logThread.isAlive() is False:
            # Change Button Text
            self.logButton.config(text="Start Logging")
            # Tell user logging has stopped
            print("Logging Stopped - Success!")
            # Re-enable Button
            self.logButton['state'] = 'normal'
        else:
            # Repeat the process after a certain period of time.
            # Note that time.sleep isn't used here. This is Crucial to why this has been done
            # The timer works independently to the main thread, allowing the print statments to be processed
            # This stops the program freezing if logThread is trying to print but the GUI is occupied so it can't
            self.after(100, self.logThreadStopCheck)

    # This redirects all print statements from console to the textbox in the GUI.
    # Note - errors will be displayed in terminal still
    # It essentially redefines what the print statement does
    def redirector(self, inputStr):
        # Enable, write data, delete unnecessary data, disable
        self.liveDataText['state'] = 'normal'
        self.liveDataText.insert(END, inputStr)
        # If over a certain amount of lines, delete all lines from the top up to a threshold
        self.textIndex = float(self.liveDataText.index('end'))
        if self.textIndex > self.textThreshold:
            self.liveDataText.delete(1.0, self.textIndex - self.textThreshold)
            # Remove history from RAM (to avoid memory Leak
            self.liveDataText.edit_reset()
        self.liveDataText['state'] = 'disabled'
        # If autoscroll is enabled, then scroll to bottom
        if self.autoScrollEnable.get() == 1:
            self.liveDataText.see(END)

    # Make sure logging finishes before program closes
    def onClose(self):
        errorLogger = logging.getLogger('error_logger')
        try:
            if logger.logEnbl is True:
                close = messagebox.askokcancel("Close", "Logging has not be finished. Are you sure you want to quit?")
                if close:
                    self.logToggle()
                    root.destroy()
                    errorLogger.info("\nGUI Closed Successfully")
            else:
                root.destroy()
                errorLogger.info("\nGUI Closed Successfully")
        # If logger has never been run, logger.logEnbl will not exist
        except AttributeError:
            root.destroy()
            errorLogger.info("\nGUI Closed Successfully")


# Setup error logging
def errorLoggingSetup():
    # Used to set logger
    errorLogger = logging.getLogger('error_logger')
    # Select min level of severity to log
    errorLogger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('piError.log')
    fh.setLevel(logging.INFO)
    errorLogger.addHandler(fh)
    # Print Top Line to make it easy to identify new instance of program
    errorLogger.info("\n\n{}\nNEW INSTANCE OF LOGGER GUI @ {}\n{}\n".format('-' * 75, datetime.now(), '-' * 75))


# Function called every time a line of an error is written to sys.stderr
# Redirects them from the (invisible) console to the log file
# Note: - Function may be called once per error (if error originates in a separate thread)
# or several times until error is written.
def stderrRedirect(buf):
    # Setup error logging
    errorLogger = logging.getLogger('error_logger')
    # Print Stderr to error logger with a timestamp
    for line in buf.rstrip().splitlines():
        errorLogger.error("{}  - {}".format(datetime.now(), line.rstrip()))
    # Show Message Box in Program to warn user of error - note several may appear for a given error
    messagebox.showerror("Error", "More Unhandled Exceptions! Check piError.log"
                                      "\nNote: This message may appear several times for a given error")


# PROGRAM START #
# Start Error Logging
errorLoggingSetup()

# Warn Users of error locations
print("Warning - all stderr output from this point onwards is logged in piError.log")
# Redirect all stderr to text file. Comment the next line out for errors to be written to the console
sys.stderr.write = stderrRedirect

# Create Tkinter Instance
root = Tk()

# Set Window Icon
img = PhotoImage(file='icon.png')
root.tk.call('wm', 'iconphoto', root._w, img)

# Size of the window (Uncomment for Full Screen)
# root.wm_attributes('-zoomed', 1)

# Fonts
bigFont = font.Font(family="Helvetica", size=16, weight=font.BOLD)
smallFont = font.Font(family="Courier", size=11)

# Create instance of GUI
app = WindowTop(root)

# Ensure when the program quits, it quits gracefully - e.g. stopping the log first
root.protocol("WM_DELETE_WINDOW", app.onClose)

# Tkinter Mainloop in charge of making the gui do everything
root.mainloop()
