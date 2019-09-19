import sys
import logging
from datetime import datetime
import tkinter


# Setup error logging
def errorLoggingSetup():
    # Used to set logger
    errorLogger = logging.getLogger('error_logger')
    # Select min level of severity to log
    errorLogger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.INFO)
    errorLogger.addHandler(fh)
    # Print Top Line to make it easy to identify new instance of program
    errorLogger.info("\n{}\nNEW INSTANCE OF UI @ {}\n{}\n".format('-' * 75, datetime.now(), '-' * 75))


# Function called every time a line of an error is written to sys.stderr
# Redirects them from the (invisible) console to the log file
def stderrRedirect(buf):
    # Setup error logging
    errorLogger = logging.getLogger('error_logger')
    # Print Stderr to error logger with a timestamp
    for line in buf.rstrip().splitlines():
        errorLogger.error("{}  - {}".format(datetime.now(), line.rstrip()))


def init():
    # Start Error Logging
    errorLoggingSetup()
    # Redirect all stderr to text file
    sys.stderr.write = stderrRedirect
    top = tkinter.Tk()
    w = tkinter.Button(top, text="Cause Exception", command=exception)
    w.pack()
    top.mainloop()


def exception():
    raise Exception("Test")

if __name__ == "__main__":
    init()
    print("Hello")
