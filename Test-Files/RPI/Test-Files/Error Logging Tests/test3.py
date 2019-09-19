import sys
import logging
from datetime import datetime


# Setup error logging
# Note exceptions will print to console when running from Thonny IDE! To test, run script from GUI
def errorLoggingSetup():
    # Used to set logger
    errorLogger = logging.getLogger('error_logger')
    # Select min level of severity to log
    errorLogger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('error.log')
    fh.setLevel(logging.INFO)
    errorLogger.addHandler(fh)
    # Print Top Line to make it easy to identify new instance of program
    errorLogger.info("\n\n{}\nNEW INSTANCE OF LOGGER GUI @ {}\n{}".format('-'*75, datetime.now(), '-'*75))


def write(buf):
    errorLogger = logging.getLogger('error_logger')
    for line in buf.rstrip().splitlines():
        errorLogger.error(line.rstrip())


errorLoggingSetup()

sys.stderr.write = write

sys.stderr.write("Hello\nThis\nIs\na\ntest")