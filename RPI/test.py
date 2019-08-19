import logging
import sys
from datetime import datetime

# Setup error logging
# Note exceptions will print to console when running from Thonny IDE! To test, run script from GUI
def errorLoggingSetup():
    errorLogger = logging.getLogger('error_logger')
    errorLogger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('error.log')
    fh.setLevel(logging.INFO)
    errorLogger.addHandler(fh)
    # Print Top Line to make it easy to identify new instance of program
    errorLogger.info("\n{}\nNEW INSTANCE OF LOGGER @ {}\n{}\n".format('-'*75, datetime.now(), '-'*75))

# Start Logging
errorLoggingSetup()


try: 
    print("Running")
    print(dfdkhk)
except Exception:
    errorLogger = logging.getLogger('error_logger')
    print("UNHANDLED EXCEPTION - Check Log File")
    errorLogger.exception("Unhandeled Exception! \nTime/Date: {}\nDetails:\n".format(datetime.now()))