import pandas as pd
import statistics as stats
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing


class Classifier:
    def __init__(self, num_of_bins, files_folder=''):
        self.nb = MultinomialNB(alpha=2)
        self.files_folder = files_folder
        self.test_path = files_folder + '/test.csv'
        self.train_path = files_folder + '/train.csv'
        structure_path = files_folder + '/Structure.txt'
        self.num_of_bins = int(num_of_bins)
        self.model = None
        self.encoder = {}
        self.futures_struct = self.readFile(structure_path)  # key: future val: possible values
        self.feature_keys = [key for key in self.futures_struct.keys() if key != "class"]
        tmp_train_data = pd.read_csv(self.train_path)
        if tmp_train_data.shape[0] == 0 or not set(self.futures_struct.keys()).issubset(
                set(tmp_train_data.columns)):  # len(set(tmp_train_data.columns).intersection(self.futures_struct)) != len(self.futures_struct.keys()):#self.futures_struct.keys().__contains__(tmp_train_data.columns):
            raise Exception("Bad train file")
        tmp_test_data = pd.read_csv(self.test_path)
        if tmp_test_data.shape[0] == 0 or not set(self.futures_struct.keys()).issubset(
                set(tmp_test_data.columns)):  # len(set(tmp_test_data.columns).intersection(self.futures_struct)) != len(self.futures_struct.keys()):
            raise Exception("Bad test file")
        limit_ind = tmp_train_data.shape[0]
        self.allData = pd.concat([tmp_train_data, tmp_test_data])
        self.data_preProcessing()
        self.train_data = self.allData.iloc[:limit_ind, :]
        self.test_data = self.allData.iloc[limit_ind:, :]

    def readFile(self, structure_path):
        futures_struct = {}  # key: future val: possible values
        with open(structure_path) as f:
            structure_data = f.read()
            f.close()
        structure_data = structure_data.split('\n')
        for line in structure_data:
            s_line = line.split()
            s_line[2] = s_line[2].strip('{ }').split(',')
            futures_struct[s_line[1]] = s_line[2]

        return futures_struct

    def data_preProcessing(self):
        le = preprocessing.LabelEncoder()
        for feature in self.futures_struct:
            if self.futures_struct[feature][0] != "NUMERIC":
                self.encoder[feature] = le.fit(self.allData[feature])
                self.allData[feature] = self.encoder[feature].transform(self.allData[feature])
                self.allData[feature].fillna(stats.mode(self.allData[feature]), inplace=True)
            else:
                self.allData[feature].fillna(self.allData[feature].mean(), inplace=True)
                self.allData[feature] = self.binning(self.allData[feature])

    def binning(self, col):
        kBins = preprocessing.KBinsDiscretizer(self.num_of_bins, encode='ordinal')
        return kBins.fit_transform(col.values.reshape((len(col), 1)))

    def build(self):
        y_train = self.train_data.loc[:, "class"]
        X_train = self.train_data.loc[:, self.feature_keys]
        self.model = self.nb.fit(X_train, y_train)

    def classify(self):
        y_test = self.test_data.loc[:, "class"]
        X_test = self.test_data.loc[:, self.feature_keys]
        y_pred = self.model.predict(X_test)
        with open("output.txt", 'w') as file:  # Use file to refer to the file object
            ind = 1
            for res in self.encoder["class"].inverse_transform(y_pred):
                file.write("{0} {1}\n".format(ind, res))
                ind += 1
        print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
