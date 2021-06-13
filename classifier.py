import csv

import numpy
import numpy as np
import pandas as pd
import statistics as stats
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from NaiveBayesModel import Naïve_Bayes_Model
from tkinter import *
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing


class classifier:
    def __init__(self, num_of_bins, files_folder=''):
        self.nb = MultinomialNB(alpha=2)
        self.files_folder = files_folder
        self.test_path = files_folder + '/test.csv'
        self.train_path = files_folder + '/train.csv'
        structure_path = files_folder + '/Structure.txt'

        self.futures_struct = self.readFile(structure_path)  # key: future val: possible values
        self.feature_keys = [key for key in self.futures_struct.keys() if key != "class"]
        self.num_of_bins = int(num_of_bins)
        self.model = None
        self.encoder = {}

    def readFile(self, structure_path):
        futures_struct = {}  # key: future val: possible values
        with open(structure_path) as f:
            structure_data = f.read()
            f.close()
        structure_data = structure_data.split('\n')
        for line in structure_data:
            s_line = line.split()
            futures_struct[s_line[1]] = s_line[2]
            # print(s_line[1], futures_struct[s_line[1]])

        return futures_struct

    def data_preProcessing(self, data, futures_struct, num_of_bins):
        # for col in data:
        #     data[col] = data[col].astype(np.object)
        #     # data[col] = data[col].dtypes
        #     print(data[col].dtypes)
        for feature in futures_struct:
            # print(stats.mode(data[feature]))
            if data[feature].dtypes == "object" or data[feature].nunique() < 4:
                data[feature].fillna(stats.mode(data[feature]), inplace=True)
            else:
                data[feature].fillna(data[feature].mean(), inplace=True)
                data[feature] = self.binning(data[feature])

    def binning(self, col):
        # groups_name = range(num_of_bins)
        # minval = col.min()
        # maxval = col.max()
        # # cut_points = [(maxval - minval) / 3, 2 * (maxval - minval) / 3]
        # # break_points = [minval] + cut_points + [maxval]
        # # colBin = pd.cut(col, bins=break_points, labels=groups_name, include_lowest=True)
        # # return colBin
        # bins = numpy.linspace(minval, maxval, self.num_of_bins)
        # cut_points = (numpy.histogram(col, bins, weights=col)[0] /
        #               numpy.histogram(col, bins)[0])
        # break_points = np.insert(cut_points, 0, minval)
        # break_points = np.insert(break_points, len(break_points), maxval)

        # colBin = pd.cut(col, bins=break_points, labels=groups_name, duplicates='drop', include_lowest=True)
        kBins = preprocessing.KBinsDiscretizer(self.num_of_bins, encode='ordinal')
        return kBins.fit_transform(col.values.reshape((len(col),1)))

    # def apreiory(futures_struct, numberOfRows, train_data):
    #     probabilty_dict = dict()
    #     for feateure in futures_struct.keys():
    #         feateure_dict = train_data[feateure].value_counts()
    #         for atrribute in feateure_dict.keys():
    #             feateure_atrribute = "{0}_{1}".format(feateure, atrribute)
    #             probabilty_dict[feateure_atrribute] = feateure_dict[atrribute] / numberOfRows
    #     return probabilty_dict
    #
    #
    # def condintional_probabilty(futures_struct, train_data):
    #     probabilty_df = pd.DataFrame(columns=["Y", "N"])
    #     m_estimte = 2
    #     feature_class = train_data["class"].value_counts()
    #     mp = 2 / len(feature_class.keys())
    #     futures_struct.pop("class")
    #     for feateure in futures_struct.keys():
    #         feateure_dict = train_data[feateure].value_counts()
    #         for atrribute in feateure_dict.keys():
    #             feateure_atrribute = "{0}_{1}".format(feateure, atrribute)
    #             num_of_samples_with_attribute_and_yes = train_data.loc[
    #                 (train_data[feateure] == atrribute) & (train_data["class"] == "Y")].count()
    #             num_of_samples_with_attribute_and_no = train_data[
    #                 (train_data[feateure] == atrribute) & (train_data["class"] == "N")].count()
    #             ans_class_yes = (mp + (num_of_samples_with_attribute_and_yes)) / ((feature_class["Y"]) + m_estimte)
    #             ans_class_no = (mp + (num_of_samples_with_attribute_and_no)) / ((feature_class["N"]) + m_estimte)
    #             probabilty_df.loc[feateure_atrribute, "Y"] = ans_class_yes[feateure]
    #             probabilty_df.loc[feateure_atrribute, "N"] = ans_class_no[feateure]
    #     return probabilty_df
    #
    #
    # def classifier(condintional_probabilty_df, apri_class_dict, class_val, record):
    #     final_prob_list = {}
    #     for value in class_val:
    #         final_prob_list[value] = apri_class_dict["class_" + value.__str__()]
    #         for key, val in record.iteritems():
    #             if key == "class":
    #                 continue
    #             ind = key.__str__() + '_' + val.__str__()
    #             final_prob_list[value] *= condintional_probabilty_df.loc[ind, value]
    #     return max(final_prob_list, key=final_prob_list.get)
    #
    #
    # def predict(condintional_probabilty_df, apreiory_probabilty_dict, class_val, test_data):
    #     output_arg = []
    #     with open("output.txt", 'w') as file:  # Use file to refer to the file object
    #         for index, row in test_data.iterrows():
    #             classify = classifier(condintional_probabilty_df, apreiory_probabilty_dict, class_val, row)
    #             # output_arg.append(classify)
    #             file.write("{0} {1}\n".format(index + 1, classify))

    def test_discrate(self, test_data):
        for col in test_data:
            if test_data[col].dtypes == "object" or test_data[col].nunique() < 4:
                continue
            else:
                test_data[col] = self.binning(test_data[col])

    def build(self):
        train_data = pd.read_csv(self.train_path)
        self.data_preProcessing(train_data, self.futures_struct, self.num_of_bins)
        # class_val = (futures_struct["class"].strip("} {")).split(',')
        # apreiory_probabilty_dict = apreiory(futures_struct, numberOfRows,
        #                                     train_data)  # key: column Name and Feather name val: probabilty
        # condintional_probabilty_df = condintional_probabilty(futures_struct, train_data)
        # predict(condintional_probabilty_df, apreiory_probabilty_dict, class_val, test_data)
        for key, val in self.futures_struct.items():
            if train_data[key].dtype == "object":
                le = preprocessing.LabelEncoder()
                self.encoder[key] = le.fit(train_data[key])
                train_data[key] = self.encoder[key].transform(train_data[key])
        y_train = train_data.loc[:, "class"]
        X_train = train_data.loc[:, self.feature_keys]

        self.model = self.nb.fit(X_train, y_train)

    def classify(self):
        """files reader"""
        test_data = pd.read_csv(self.test_path)
        self.data_preProcessing(test_data, self.futures_struct, self.num_of_bins)
        for key, val in self.futures_struct.items():
            if test_data[key].dtype == "object":
                test_data[key] = self.encoder[key].transform(test_data[key])
        y_test = test_data.loc[:, "class"]
        X_test = test_data.loc[:, self.feature_keys]
        y_pred = self.model.predict(X_test)
        with open("output.txt", 'w') as file:  # Use file to refer to the file object
            ind = 1
            for res in self.encoder["class"].inverse_transform(y_pred):
                file.write("{0} {1}\n".format(ind, res))
                ind += 1
        print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
