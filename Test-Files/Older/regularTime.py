import time
timeDelay = float(input("How Long?\n"))
starttime=time.time()
while True:
  print("tick")
  time.sleep(timeDelay - ((time.time() - starttime) % timeDelay))
