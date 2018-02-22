from datetime import datetime
import csv
import os

print("Gyro: {}, {}, {}  [deg/s]".format("Test1", "Test2", "Test3"))
print("Accel: {}, {}, {}  [Gs]".format("Test1", "Test2", "Test3"))

filename = "/home/pi/data_log.csv"
write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0

with open(filename, "a", newline="") as f_output:
    csv_output = csv.writer(f_output)

    if write_header:
        csv_output.writerow(["Time", "Gyro", "Accel", "Mag"])

    while True:
        row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cgx, cgy, cgz, cax, cay, caz, cmx, cmy, cgz]
        csv_output.writerow(row)
        time.sleep(5)
