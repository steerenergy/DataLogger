import csv
import time

x = 1
potato = ["potato1", "potato 2", "potato 3",]
with open('TEST.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for x in range(3):
        writer.writerow(potato);
        print("Done");
        time.sleep(0.5);
        print(potato);

print("All Finished");
