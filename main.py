import csv

import pandas as pd

'''files reader'''

test_path = 'test.csv'
train_path = 'train.csv'
structure_path = 'Structure.txt'
test_data = pd.read_csv(test_path)
train_data = pd.read_csv(train_path)
futures_struct = {} # key: future val: possible values
with open(structure_path) as f:
    structure_data = f.read()
    f.close()
structure_data = structure_data.split('\n')
for line in structure_data:
    s_line = line.split()
    futures_struct[s_line[1]] = s_line[2]
