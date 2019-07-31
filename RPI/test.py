import sys
sys.stderr = open('error.txt', 'w')
sys.stderr.write("THIS IS AN ERROR")