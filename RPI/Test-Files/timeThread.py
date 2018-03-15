import threading
import datetime

def printit():
  threading.Timer(1.0, printit).start()
  print(datetime.datetime.now())

printit();
