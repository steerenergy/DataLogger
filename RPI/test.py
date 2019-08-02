import logging
import sys

# Setup error logging
logger = logging.getLogger('error_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('error.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def exception_handler(exc_type, exc_value, exc_traceBack):
    print("UNANDELED EXCEPTION - Check Log File")
    logger.error("Unhandled Exception!\nType: {}\nValue: {}\nTraceback: {}\n".format(exc_type, exc_value, exc_traceBack))

# Redirect Exceptions to text file
sys.excepthook = exception_handler

print("Running")
raise RuntimeError