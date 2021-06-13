from tkinter import *
# import filedialog module
from tkinter import filedialog
from classifier import classifier


class Naïve_Bayes_Classifier:

    def __init__(self):
        self.master = Tk()
        self.master.title("Naïve Bayes Classifier")
        self.master.configure(bg='white')
        # self.master.geometry("600x400")
        self.master.resizable(0, 0)
        self.master.grid_columnconfigure(0, weight=5)
        self.master.grid_rowconfigure(0, weight=5)
        self.classifier = None
        # self.frame = Frame(self.master)
        # self.frame.pack(expand=1, fill='both')

        # self.total = 0
        # self.entered_number = 0

        # self.total_label_text = IntVar()
        # self.total_label_text.set(self.total)
        # self.total_label = Label(master, textvariable=self.total_label_text)

        self.label_browse = Label(self.master, text="Directory Path", bg='white')
        self.label_bins = Label(self.master, text="Discretization Bins:", bg='white')

        vcmd = self.master.register(self.validate)  # we have to wrap the command
        self.entry_bins = Entry(self.master, validate="key")
        # self.folderString = StringVar()
        self.entry_browser = Entry(self.master, validate="key")

        self.build_button = Button(self.master, text="Build", command=lambda: self.build())
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
        self.classifier = classifier(self.entry_bins.get(), self.entry_browser.get())
        self.classifier.build()
        self.classify_button["state"] = "normal"

    def classify(self):
        self.classifier.classify()

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
        filename = filedialog.askdirectory()
        self.entry_browser.insert(END, filename)

        # # Change label contents
        # label_file_explorer.configure(text="File Opened: " + filename)


if __name__ == '__main__':
    my_gui = Naïve_Bayes_Classifier()
