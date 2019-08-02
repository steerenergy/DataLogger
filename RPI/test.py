""" import logging
import sys

logger = logging.getLogger('error_logger')
def exception_handler(exc_type, exc_value, exc_traceBack):
    logger.exception("Unhandled Exception! - Type: {}\n Value: {}\n Traceback: {}".format(exc_type, exc_value, exc_traceBack))

# Redirect Exceptions to text file
sys.excepthook = exception_handler

print("Running")
raise RuntimeError """


import logging
import sys

logger = logging.getLogger('mylogger')
# Configure logger to write to a file...

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))

# Install exception handler
sys.excepthook = my_handler

# Run your main script here:
if __name__ == '__main__':
    main()