# Contains common commands used by other programs to reduce code
import sys


def quit():
    print("\nGoodbye :)\n")
    sys.exit()


def back():
    raise StopIteration()


def other():
    print("Invalid Option. Please Try Again")
