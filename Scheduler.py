from Process import *
import numpy as np


class Scheduler:
    def __init__(self, processes, switchTime=0, rrQuantum=0):
        self.processes = processes
        self.switchTime = switchTime
        self.rrQuantum = rrQuantum
        self.finishList = []

    def schedule(self, TYPE):
        if TYPE == "HPF":
            self.HPF()
        elif TYPE == "FCFS":
            self.FCFS()
        elif TYPE == "RR":
            self.RR()
        elif TYPE == "SRTN":
            self.SRTN()
        else:
            return

    def FCFS(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        lastTime = self.processes[0].arrivalTime
        for process in self.processes:
            print("Process " + str(process.num) + " begins at : " + str(lastTime))
            process.waitingTime += lastTime - process.arrivalTime  # waiting = start - arrival
            process.status = 0
            lastTime += process.burstTime
            process.tat += lastTime - process.arrivalTime  # turn around time = finish - arrival
            process.weightedTAT = process.tat / process.burstTime
            print("Process " + str(process.num) + " ends at : " + str(lastTime))
            lastTime += self.switchTime

    def HPF(self):
        pass

    def RR(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        self.finishList = []
        queue = self.processes.copy()
        queue.reverse()
        lastTime = self.processes[0].arrivalTime
        while len(queue) > 0:
            process = queue.pop()
            print("Process " + str(process.num) + " begins at : " + str(lastTime))
            execTime = min(self.rrQuantum, process.remaining)
            process.remaining -= execTime
            process.waitingTime += lastTime - process.last
            lastTime += execTime
            process.last = lastTime
            if process.remaining <= 0:
                process.tat = process.last - process.arrivalTime
                process.weightedTAT = process.tat / process.burstTime
                self.finishList.append(process)
            else:
                queue.insert(0, process)
            print("Process " + str(process.num) + " stops at : " + str(lastTime))

    def SRTN(self):
        pass

    def printInfo(self):
        TAT = 0
        WTAT = 0
        for process in self.finishList:
            print("Process {0}: wait={1}, tat ={2} , wTat={3}".format(process.num, process.waitingTime, process.tat,
                                                                      process.weightedTAT))
            TAT += process.tat
            WTAT += process.weightedTAT
        print("Avg TAT = {0}\nAvg WTAT = {1}".format(TAT / len(self.processes), WTAT / len(self.processes)))


def main():
    scheduler = Scheduler(
        [
            Process(1, 0, 10, 8),
            Process(2, 2, 3, 8),
            Process(3, 3, 2, 8),
            Process(4, 5, 1, 8),
        ])
    scheduler.RR(2)
    scheduler.printInfo()


if __name__ == '__main__':
    main()
