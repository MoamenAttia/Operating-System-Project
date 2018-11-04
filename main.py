from tkinter import *
from pathlib import Path


class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


mainWindow = Tk()
Choice = StringVar(mainWindow)

rrQuantumEntry = EntryWithPlaceholder(mainWindow, placeholder="Quantum Value", color="grey")
rrQuantumEntry.grid(row=2, column=1, sticky='w')

switchTimeEntry = EntryWithPlaceholder(mainWindow, placeholder="switch overhead")
switchTimeEntry.grid(row=4, column=1, sticky='w')

inputFileEntry = EntryWithPlaceholder(mainWindow, placeholder="input file")
inputFileEntry.grid(row=3, column=1, sticky='w')


def change_dropdown(*args):
    print(Choice.get())
    global rrQuantumEntry
    if Choice.get() == 'RR':
        rrQuantumEntry = EntryWithPlaceholder(mainWindow, placeholder="Quantum Value", color="grey")
        rrQuantumEntry.grid(row=2, column=1, sticky='w')
        rrQuantumEntry.configure(state=NORMAL)
    else:
        rrQuantumEntry = EntryWithPlaceholder(mainWindow, placeholder="Disabled", color="grey")
        rrQuantumEntry.grid(row=2, column=1, sticky='w')
        rrQuantumEntry.configure(state=DISABLED)


def getFileName():
    global inputFileEntry
    myFileName = inputFileEntry.get()
    myFile = Path(myFileName)
    if myFile.is_file():
        print("success")
    else:
        inputFileEntry = EntryWithPlaceholder(
            mainWindow, placeholder="input file")
        inputFileEntry.grid(row=3, column=1, sticky='w')
        print("failed")


def getQuantum():
    global rrQuantumEntry
    Quantum = rrQuantumEntry.get()
    print(Quantum)


def getSwitchTime():
    global switchTimeEntry
    switchTime = switchTimeEntry.get()
    print(switchTime)


def schedule():
    getFileName()
    getQuantum()


choices = {'HPF', 'FCFS', 'RR', 'SRTN'}
popupMenu = OptionMenu(mainWindow, Choice, *choices)

scheduleButton = Button(mainWindow, text="Schedule", command=schedule)
scheduleButton.grid(row=5, sticky=W+E, columnspan=2)

mainWindow.title("Operating System Project")
mainWindow.geometry('300x120')

# Column Configuration
mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=2)

# Creating The Drop down Menu
Choice.set('RR')
Label(mainWindow, text="Choose a Scheduler").grid(row=0, column=0, sticky='w')
popupMenu.grid(row=0, column=1, sticky='w')
Label(mainWindow, text="Enter Quantum").grid(row=2, column=0, sticky='w')
Label(mainWindow, text="Enter input file").grid(row=3, column=0, sticky='w')
Label(mainWindow, text="Enter Switch Time").grid(row=4, column=0, sticky='w')
Choice.trace('w', change_dropdown)
mainWindow.mainloop()
