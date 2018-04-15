import numpy as np
import pandas as pd
import sys
sys.path.append("..")
import common

def init():
    global conversion
    conversion = {}
    conversionSetup()
    csvProcess()

def conversionSetup():
    conversion['0A1'] = 2
    conversion['0A0'] = 3

def csvProcess():
    #read CSV
    df = pd.read_csv('raw.csv')
    print("Raw Data:")
    print(df)
    for item in df.iloc[:,2:].columns:
        df[item] = df[item].apply(convert, args=(item,))
    print("\nConverted Data:")
    print(df)
    #Write Converted CSV
    df.to_csv('converted.csv', sep=',')

def convert(value,item):
    return value*conversion[item]


if __name__ == "__main__":
    init()
