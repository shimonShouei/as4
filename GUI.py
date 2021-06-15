import os
from tkinter import *
# import filedialog module
from tkinter import filedialog
from classifier import Classifier
from tkinter import messagebox


class Naïve_Bayes_Classifier:

    def __init__(self):
        self.master = Tk()
        self.master.title("Naïve Bayes Classifier")
        self.master.configure(bg='white')
        self.master.resizable(0, 0)
        self.master.grid_columnconfigure(0, weight=5)
        self.master.grid_rowconfigure(0, weight=5)
        self.classifier = None
        self.label_browse = Label(self.master, text="Directory Path", bg='white')
        self.label_bins = Label(self.master, text="Discretization Bins:", bg='white')

        vcmd = self.master.register(self.validate)  # we have to wrap the command
        vcmd1 = self.master.register(self.validateFolder)  # we have to wrap the command
        self.entry_bins = Entry(self.master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry_browser = Entry(self.master, validate="key", validatecommand=(vcmd1, '%S'))

        self.build_button = Button(self.master, text="Build", command=lambda: self.build(), state="disabled")
        self.classify_button = Button(self.master, text="Classify", command=lambda: self.classify(), state="disabled")

        # Button label
        self.browse_button = Button(self.master, text='Browse', command=lambda: self.browseFiles())

        # LAYOUT

        self.label_browse.grid(row=2, column=4, sticky=NSEW)
        self.label_bins.grid(row=4, column=4, sticky=NSEW)

        self.entry_bins.grid(row=4, column=5, sticky=NSEW)
        self.entry_browser.grid(row=2, column=5, sticky=NSEW)
        self.build_button.grid(row=6, column=5, sticky=NSEW)
        self.classify_button.grid(row=8, column=5, sticky=NSEW)
        self.browse_button.grid(row=2, column=6, sticky=NSEW)
        self.master.mainloop()

    def build(self):
        try:
            self.classifier = Classifier(self.entry_bins.get(), self.entry_browser.get())
        except Exception:
            messagebox.showinfo("Naïve Bayes Classifier", "One of the files are bad")
            return

        self.classifier.build()
        self.classify_button["state"] = "normal"
        messagebox.showinfo("Naïve Bayes Classifier", "Building classifier using train-set is done")

    def classify(self):
        self.classifier.classify()
        messagebox.showinfo("Naïve Bayes Classifier", "Process is done")

    def validate(self, new_text):
        flag = new_text.isdigit() and int(new_text) > 0
        if flag:
            self.build_button["state"] = "normal"
        else:
            self.build_button["state"] = "disabled"
            messagebox.showerror("Naïve Bayes Classifier", "invalid number of bins")

        return flag

    def validateFolder(self, new_text):
        listdir = os.listdir(new_text)
        if not listdir.__contains__("train.csv"):
            messagebox.showerror("Naïve Bayes Classifier", "wrong folder: train file is missing")
            return False
        if not listdir.__contains__("Structure.txt"):
            messagebox.showerror("Naïve Bayes Classifier", "wrong folder: Structure file is missing")
            return False
        if not listdir.__contains__("test.csv"):
            messagebox.showerror("Naïve Bayes Classifier", "wrong folder: test file is missing")
            return False

        else:
            return True

    def browseFiles(self):
        files_folder = filedialog.askdirectory()
        self.entry_browser.delete(0, END)
        self.entry_browser.insert(END, files_folder)


if __name__ == '__main__':
    my_gui = Naïve_Bayes_Classifier()
