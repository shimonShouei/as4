import csv

import pandas as pd
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from as4.GUI import Naïve_Bayes_Classifier
from as4.NaiveBayesModel import Naïve_Bayes_Model
from tkinter import *

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
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # window = tk.Tk()
    # # window.title("Naïve Bayes Classifier")
    # # greeting = tk.Label(text="Hello, Tkinter")
    # # entry = tk.Entry(fg="black", bg="white", width=40)
    # # entry.place(x=20,y=10)
    # # greeting.pack()
    # # entry.pack()
    #
    #
    # T1 = tk.Text(window)
    # T1.tag_configure("center", justify='center')
    # T1.insert("1.0", "text")
    # T1.tag_add("center", "1.0", "end")
    # T1.pack()
    # window.mainloop()
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    my_gui = Naïve_Bayes_Classifier(root)
    root.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
