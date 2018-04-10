#System Comands
import sys

def quit():
    print("\nGoodbye :)\n")
    sys.exit()

def back():
    raise StopIteration()

def other():
    print("Invalid Option. Please Try Again")
