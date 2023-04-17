from geneticalgorithm import geneticalgorithm
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='fit model using to experimental data using the genetic algorithm')
parser.add_argument('-i', '--input', help='input experimental fit data', required=True)

def openData(path):
    df = pd.read_csv(path, header=0)
    return df

def costFunction(parameters):




if __name__ == '__main__':
    args = parser.parse_args()
    df = openData(args.input)
    print(df)
