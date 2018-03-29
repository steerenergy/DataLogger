import time

def init():
    list = ["item1","item2","item3","item4"]
    property = ["prop1","prop2","prop 3","prop 4"]
    print("\nWelcome to the Config Editor \nHere are the current settings:")

    while True:
        for x in list:
            print("|{:>5}|".format(x))
        time.sleep(0.2)
        list.append("spam")
if __name__ == "__main__":
        init()

#DO 2D ARRAY NEXT
