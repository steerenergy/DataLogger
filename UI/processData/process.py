import numpy as np
import pandas as pd
import sys
sys.path.append("..")
import common

def convert(value):
    return value*2

def init():
    #Read read CSV
    df = pd.read_csv('raw.csv')
    print("Raw Data:")
    print(df)
    for item in df.iloc[:,2:].columns:
        df[item] = df[item].apply(convert)
    print("\nConverted Data:")
    print(df)
    #Write Converted CSV
    df.to_csv('converted.csv', sep=',')

if __name__ == "__main__":
    init()
