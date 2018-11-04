from tkinter import *

mainWindow = Tk()
Choice = StringVar(mainWindow)
rrQuantum = StringVar(mainWindow)
inputFile = StringVar(mainWindow)
rrQuantumEntry = Entry(mainWindow, textvariable=rrQuantum, state=DISABLED).grid(row=2, column=1, sticky='e')
switchTime = StringVar(mainWindow)
switchTimeEntry = Entry(mainWindow, textvariable=switchTime).grid(row=4, column=1, sticky='e')


def change_dropdown(*args):
    print(Choice.get())
    global rrQuantumEntry
    if Choice.get() == 'RR':
        rrQuantumEntry = Entry(mainWindow, textvariable=rrQuantum, state=NORMAL).grid(row=2, column=1, sticky='e')


def change_input(*args):
    inputFile.trace('w', change_input)


def getFileName(*args):
    inputFile.trace('w', change_input)
    return inputFile


def schedule():
    print(getFileName().get())


choices = {'HPF', 'FCFS', 'RR', 'SRTN'}
popupMenu = OptionMenu(mainWindow, Choice, *choices)
inputFileEntry = Entry(mainWindow, textvariable=inputFile).grid(row=3, column=1, sticky='e')
scheduleButton = Button(mainWindow, text="Schedule", command=schedule).grid(row=5, sticky='n')
mainWindow.title("Operating System Project")

# Column Configuration
mainWindow.columnconfigure(0, weight=1)
mainWindow.columnconfigure(1, weight=2)

# Creating The Drop down Menu
Choice.set('HPF')
Label(mainWindow, text="Choose a Scheduler").grid(row=0, column=0)
popupMenu.grid(row=0, column=1, sticky='w')
Label(mainWindow, text="Enter Quantum").grid(row=2, column=0)
Label(mainWindow, text="Enter input file").grid(row=3, column=0)
Label(mainWindow, text="Enter Switch Time").grid(row=4, column=0)
Choice.trace('w', change_dropdown)
inputFile.set('input.txt')
mainWindow.mainloop()
