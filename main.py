import csv

import numpy as np
import pandas as pd
import statistics as stats
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from GUI import Naïve_Bayes_Classifier
from NaiveBayesModel import Naïve_Bayes_Model
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
        if data[feature].dtypes == "object" or data[feature].nunique() < 4:
            data[feature].fillna(stats.mode(data[feature]), inplace=True)
        else:
            data[feature].fillna(data[feature].mean(), inplace=True)
            data[feature] = binning(data[feature])


def binning(col):
    groups_name = [0, 1, 2]
    minval = col.min()
    maxval = col.max()
    cut_points = [(maxval - minval) / 3, 2 * (maxval - minval) / 3]
    break_points = [minval] + cut_points + [maxval]
    colBin = pd.cut(col, bins=break_points, labels=groups_name, include_lowest=True)
    return colBin


def apreiory(futures_struct, numberOfRows, train_data):
    probabilty_dict = dict()
    for feateure in futures_struct.keys():
        feateure_dict = train_data[feateure].value_counts()
        for atrribute in feateure_dict.keys():
            feateure_atrribute = "{0}_{1}".format(feateure, atrribute)
            probabilty_dict[feateure_atrribute] = feateure_dict[atrribute] / numberOfRows
    return probabilty_dict


def condintional_probabilty(futures_struct, train_data):
    probabilty_df = pd.DataFrame(columns=["Y", "N"])
    m_estimte = 2
    feature_class = train_data["class"].value_counts()
    mp = 2 / len(feature_class.keys())
    futures_struct.pop("class")
    for feateure in futures_struct.keys():
        feateure_dict = train_data[feateure].value_counts()
        for atrribute in feateure_dict.keys():
            feateure_atrribute = "{0}_{1}".format(feateure, atrribute)
            num_of_samples_with_attribute_and_yes = train_data[
                (train_data[feateure] == atrribute) & (train_data["class"] == "Y")].count()
            num_of_samples_with_attribute_and_no = train_data[
                (train_data[feateure] == atrribute) & (train_data["class"] == "N")].count()
            ans_class_yes = (mp + (num_of_samples_with_attribute_and_yes) / (feature_class["Y"]) + m_estimte)
            ans_class_no = (mp + (num_of_samples_with_attribute_and_no) / (feature_class["N"]) + m_estimte)
            probabilty_df.loc[feateure_atrribute, "Y"] = ans_class_yes[feateure]
            probabilty_df.loc[feateure_atrribute, "N"] = ans_class_no[feateure]
    return probabilty_df


def classifier(condintional_probabilty_df, apri_class_dict, class_val, record):
    final_prob_list = {}
    for value in class_val:
        final_prob_list[value] = apri_class_dict["class_" + value.__str__()]
        for key, val in record.iteritems():
            if key == "class":
                continue
            ind = key.__str__() + '_' + val.__str__()
            final_prob_list[value] *= condintional_probabilty_df.loc[ind, value]
    return max(final_prob_list, key=final_prob_list.get)


def predict(condintional_probabilty_df, apreiory_probabilty_dict, class_val, test_data):
    output_arg = []
    with open("output.txt", 'w') as file:  # Use file to refer to the file object
        for index, row in test_data.iterrows():
            classify = classifier(condintional_probabilty_df, apreiory_probabilty_dict, class_val, row)
            # output_arg.append(classify)
            file.write("{0} {1}\n".format(index + 1, classify))

def test_discrate(test_data):
    for col in test_data:
        if test_data[col].dtypes == "object" or test_data[col].nunique() < 4:
            continue
        else:
            test_data[col] = binning(test_data[col])

def main():
    '''files reader'''

    test_path = 'test.csv'
    train_path = 'train.csv'
    structure_path = 'Structure.txt'
    test_data = pd.read_csv(test_path)
    train_data = pd.read_csv(train_path)
    data_shape = train_data.shape
    futures_struct = readFile(structure_path)  # key: future val: possible values
    data_preProcessing(train_data, futures_struct)
    data_preProcessing(test_data, futures_struct)
    numberOfRows = data_shape[0] - 1
    class_val = (futures_struct["class"].strip("} {")).split(',')
    apreiory_probabilty_dict = apreiory(futures_struct, numberOfRows,
                                        train_data)  # key: column Name and Feather name val: probabilty
    condintional_probabilty_df = condintional_probabilty(futures_struct, train_data)
    predict(condintional_probabilty_df, apreiory_probabilty_dict, class_val, test_data)


if __name__ == '__main__':
    root = Tk()
    my_gui = Naïve_Bayes_Classifier(root)
    root.mainloop()
    main()
