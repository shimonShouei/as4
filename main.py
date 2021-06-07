import csv

import numpy as np
import pandas as pd
import statistics as stats
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from as4.GUI import Naïve_Bayes_Classifier
from as4.NaiveBayesModel import Naïve_Bayes_Model
from tkinter import *

def readFile(structure_path):
    futures_struct = {}  # key: future val: possible values
    with open(structure_path) as f:
        structure_data = f.read()
        f.close()
    structure_data = structure_data.split('\n')
    for line in structure_data:
        s_line = line.split()
        futures_struct[s_line[1]] = s_line[2]
        print(s_line[1], futures_struct[s_line[1]])

    return futures_struct

def data_preProcessing(data, futures_struct):
    # for col in data:
    #     data[col] = data[col].astype(np.object)
    #     # data[col] = data[col].dtypes
    #     print(data[col].dtypes)
    for feature in futures_struct:
        print(stats.mode(data[feature]))
        if(data[feature].dtypes == "object"):
            data[feature].fillna(stats.mode(data[feature]), inplace=True)
        else:
            data[feature].fillna(data[feature].mean(), inplace=True)

def postpreiory(futures_struct, numberOfRows, train_data):
    probabilty_dict = dict()
    for feateure in futures_struct.keys():
        feateure_dict = train_data[feateure].value_counts()
        # print(feateure_dict)
        for atrribute in feateure_dict.keys():
            feateure_atrribute = "{0}_{1}".format(feateure, atrribute)
            probabilty_dict[feateure_atrribute] = feateure_dict[atrribute] / numberOfRows

def main():
    '''files reader'''

    test_path = 'test.csv'
    train_path = 'train.csv'
    structure_path = 'Structure.txt'
    test_data = pd.read_csv(test_path)
    train_data = pd.read_csv(train_path)
    data_shape= train_data.shape
    futures_struct = readFile(structure_path)  # key: future val: possible values
    data_preProcessing(train_data, futures_struct)
    numberOfRows = data_shape[0] - 1
    postpreiory_probabilty_dict = postpreiory(futures_struct, numberOfRows) # key: column Name and Feather name val: probabilty
    condintional_probabilty_dict = {}


if __name__ == '__main__':
    root = Tk()
    my_gui = Naïve_Bayes_Classifier(root)
    root.mainloop()
    main()
