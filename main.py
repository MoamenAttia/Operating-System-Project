from tkinter import *
from pathlib import Path
import numpy as np
from Scheduler import Scheduler
from Process import Process


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
rrQuantumEntry = EntryWithPlaceholder(mainWindow, placeholder="0", color="grey")
switchTimeEntry = EntryWithPlaceholder(mainWindow, placeholder="switch overhead")
inputFileEntry = EntryWithPlaceholder(mainWindow, placeholder="input file")
processesList = []
Choice = StringVar(mainWindow)


def change_dropdown(*args):
    print(Choice.get())
    global rrQuantumEntry
    if Choice.get() == 'RR':
        rrQuantumEntry = EntryWithPlaceholder(
            mainWindow, placeholder="0", color="grey")
        rrQuantumEntry.grid(row=2, column=1, sticky='w')
        rrQuantumEntry.configure(state=NORMAL)
    else:
        rrQuantumEntry = EntryWithPlaceholder(
            mainWindow, placeholder="Disabled", color="grey")
        rrQuantumEntry.grid(row=2, column=1, sticky='w')
        rrQuantumEntry.configure(state=DISABLED)


def generateProcesses(inputFile):
    global processesList
    lines = [line.rstrip('\n') for line in open(inputFile)]
    for i in range(len(lines)):
        lines[i] = lines[i].split(' ')

    size = int(lines[0][0])
    mu = float(lines[1][0])
    sigma = float(lines[1][1])
    arrivalTime = abs(np.random.normal(mu, sigma, size))

    mu = float(lines[2][0])
    sigma = float(lines[2][1])
    burstTime = abs(np.random.normal(mu, sigma, size))

    lam = float(lines[3][0])
    priority = abs(np.random.poisson(lam, size))

    with open("output.txt", "w") as file:
        file.write(str(size) + '\n')

        for i in range(size):
            line = str(i + 1) + ' ' + str(abs(arrivalTime[i])) + ' ' + str(abs(burstTime[i])) + ' ' + str(
                abs(priority[i])) + '\n'
            file.write(line)
            processesList.append(Process(i + 1, arrivalTime[i], burstTime[i], priority[i]))


def getFileName():
    global inputFileEntry
    myFileName = inputFileEntry.get()
    myFile = Path(myFileName)
    if myFile.is_file():
        generateProcesses(myFile)
    else:
        inputFileEntry = EntryWithPlaceholder(mainWindow, placeholder="input file")
        inputFileEntry.grid(row=3, column=1, sticky='w')
        print("failed")


def getQuantum():
    global rrQuantumEntry
    Quantum = rrQuantumEntry.get()
    if Quantum == "Disabled":
        return 0
    return int(Quantum)


def getSwitchTime():
    global switchTimeEntry
    switchTime = switchTimeEntry.get()
    return int(switchTime)


def schedule():
    getFileName()
    scheduler = Scheduler(processesList, getSwitchTime(), getQuantum())
    scheduler.schedule(Choice.get())


def main():
    mainWindow.title("Operating System Project")
    mainWindow.geometry('300x120')

    rrQuantumEntry.grid(row=2, column=1, sticky='w')
    switchTimeEntry.grid(row=4, column=1, sticky='w')

    inputFileEntry.grid(row=3, column=1, sticky='w')

    # Column Configuration
    mainWindow.columnconfigure(0, weight=1)
    mainWindow.columnconfigure(1, weight=2)

    choices = {'HPF', 'FCFS', 'RR', 'SRTN'}
    popupMenu = OptionMenu(mainWindow, Choice, *choices)

    scheduleButton = Button(mainWindow, text="Schedule", command=schedule)
    scheduleButton.grid(row=5, sticky=W + E, columnspan=2)

    # Creating The Drop down Menu
    Choice.set('RR')
    Label(mainWindow, text="Choose a Scheduler").grid(row=0, column=0, sticky='w')
    popupMenu.grid(row=0, column=1, sticky='w')
    Label(mainWindow, text="Enter Quantum").grid(row=2, column=0, sticky='w')
    Label(mainWindow, text="Enter input file").grid(row=3, column=0, sticky='w')
    Label(mainWindow, text="Enter Switch Time").grid(row=4, column=0, sticky='w')
    Choice.trace('w', change_dropdown)
    mainWindow.mainloop()


if __name__ == '__main__':
    main()
