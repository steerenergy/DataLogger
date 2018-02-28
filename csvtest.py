import csv
import time

x = 0
writer = csv.writer(open("some.csv", "w"));
for x in range(0,3):
    writer.writerow(['Spam']*5);
    print("Done");
    time.sleep(500);
