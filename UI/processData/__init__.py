import sys
import csv
#Makes all directory references up a level to simplify importing common files
sys.path.append("..")
#Import Common Comands
import common

#Initial Menu Setup
def init():
    try:
        while True:
            option = input("\nProcess Data Menu: \nChoose a Option (based on the correspnding number): \n1. Download\n2. Process\n3. Back\n4. Quit \n\nOption Chosen: ")
            #Set Menu Names
            if option == "1":
                download()
            elif option == "2":
                process()
            elif option == "3":
                common.back()
            elif option == "4":
                common.quit()
            else:
                common.other()
    except StopIteration:
        pass

def download():
    pass


def process():
    #Open Raw CSV and generate list of new data to be printed
    convertedCsvData = []
    with open('raw.csv', newline='') as csvfile:
        rawCSV = csv.reader(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        newData = []
        for index, data in enumerate(rawCSV):
            for index,item in enumerate(data):
                 newData.append(item*2)
            convertedCsvData.append(newData)

    #Print New CSV
    with open('converted.csv','w', newline='') as csvfile:
        convertedCsv = csv.writer(csvfile, dialect="excel", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        convertedCsv.writerows(convertedCsvData)
if __name__ == "__main__":
    init()
