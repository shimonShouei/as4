from tkinter import *
# import filedialog module
from tkinter import filedialog


class Naïve_Bayes_Classifier:

    def __init__(self, master):
        self.master = master
        master.title("Naïve Bayes Classifier")
        self.master.configure(bg='white')
        self.master.geometry("800x400")

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label_browse = Label(master, text="Directory Path")
        self.label_bins = Label(master, text="Discretization Bins:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry_bins = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.build_button = Button(master, text="Build") #, command=lambda: self.update("add"))
        self.classify_button = Button(master, text="Classify") #, command=lambda: self.update("subtract"))

        # Button label
        self.browse_button = Button(self.master, text='Browse', command=lambda: self.browseFiles())


        # LAYOUT

        self.label_browse.grid(row=100, column=200,columnspan=2, sticky=W)
        self.label_bins.grid(row=200, column=200,columnspan=2, sticky=W)

        self.entry_bins.grid(row=200, column=270, columnspan=3, sticky=W+E)

        self.build_button.grid(row=300, column=300)
        self.classify_button.grid(row=350, column=300)
        self.browse_button.grid(row=100, column=250, sticky=W+E)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return False

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else:  # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

    # Function for opening the
    # file explorer window
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        print(input)
        for i in input:
            print(i)

        # # Change label contents
        # label_file_explorer.configure(text="File Opened: " + filename)
