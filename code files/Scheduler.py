import numpy as np
from Process import *
import matplotlib.pyplot as plt
import matplotlib


class Scheduler:
    def __init__(self, processes, switchTime=0, rrQuantum=0):
        self.processes = processes
        self.switchTime = switchTime
        self.rrQuantum = rrQuantum
        self.numProcesses = len(self.processes)
        self.finishList = []
        self.visited = []
        self.x = []
        self.y = []

    def schedule(self, TYPE):
        if TYPE == "HPF":
            self.HPF()
        elif TYPE == "FCFS":
            self.FCFS()
        elif TYPE == "RR":
            self.RR()
        elif TYPE == "SRTN":
            self.SRTN()
        self.printInfo()
        self.drawGraph()

    def FCFS(self):
        # Sort by a Custom Property
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))
        queue = self.processes.copy()
        queue.reverse()
        lastTime = self.switchTime
        self.x += [0, lastTime]
        self.y += [0, 0]
        while len(queue) > 0:
            process = queue.pop()
            if process.arrivalTime > lastTime:
                self.x += [lastTime, process.arrivalTime]
                self.y += [0, 0]
                lastTime = process.arrivalTime
            print("Process " + str(process.num) +
                  " begins at : " + str(lastTime))
            process.waitingTime += lastTime - process.arrivalTime  # waiting = start - arrival
            process.status = 0
            curr = lastTime
            lastTime += process.burstTime
            self.x += [curr, lastTime]
            self.y += [process.num, process.num]
            # turn around time = finish - arrival
            process.tat += lastTime - process.arrivalTime
            process.weightedTAT = process.tat / process.burstTime
            print("Process " + str(process.num) +
                  " ends at : " + str(lastTime))
            self.finishList += [process]
            curr = lastTime
            lastTime += self.switchTime
            if self.switchTime != 0:
                self.x += [curr, lastTime]
                self.y += [0, 0]

    def HPF(self):  # not tested or even compiled yet
        # Sort by a Custom Property
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))
        lastTime = self.switchTime
        self.x += [0, lastTime]
        self.y += [0, 0]
        # this queue holds all processes. After the execution of a process it is deleted from this queue.
        queue = self.processes.copy()
        while len(queue) > 0:
            # this list will hold the arrived processes, priority sorted
            hp = [process for process in queue if process.arrivalTime <= lastTime]
            if len(hp) == 0:
                lastTime = queue[0].arrivalTime
                self.x += [lastTime, queue[0].arrivalTime]
                self.y += [0, 0]
                continue
            # Sort processes by priority
            hp.sort(key=lambda x: (-x.priority, x.num))
            lastTime += hp[0].burstTime
            self.finishList += [hp[0]]  # should i use another [] ??
            # here we should assign the tat to the process. ask mo2men
            tat = lastTime - hp[0].arrivalTime
            self.processes[hp[0].num - 1].tat = tat
            self.processes[hp[0].num - 1].weightedTAT = tat / hp[0].burstTime
            print("Process " + str(hp[0].num) + " ends at : " + str(lastTime))
            self.x += [lastTime - hp[0].burstTime, lastTime]
            self.y += [hp[0].num, hp[0].num]
            lastTime += self.switchTime
            if self.switchTime != 0:
                self.x += [lastTime - self.switchTime, lastTime]
                self.y += [0, 0]
            queue.remove(hp[0])
            hp.remove(hp[0])

    def __fillQueue(self, queue, lastTime):
        # assumptions
        # 1 - if one process finishes its quantum and (one process or more y3ny) came at the end of execution
        # .. i choose new first

        # 2 - if one process during its execution .. new processes came .. they will be appended to queue ..
        # then append the current executing
        cnt = 1
        for i in range(self.numProcesses):
            if not (self.visited[i]) and self.processes[i].arrivalTime <= lastTime:
                self.visited[i] = True
                queue.insert(cnt, self.processes[i])
                cnt += 1

        if queue[0].remaining == 0:
            queue.remove(queue[0])

        if len(queue) == 0:
            for i in range(self.numProcesses):
                if not (self.visited[i]):
                    self.visited[i] = True
                    queue.append(self.processes[i])
                    break

    def RR(self):
        # Sort by a Custom Property
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))
        self.visited = [False] * self.numProcesses
        self.finishList = []
        queue = []
        lastTime = self.switchTime
        self.x += [0, lastTime]
        self.y += [0, 0]
        self.processes.reverse()
        curr = lastTime
        lastTime = max(lastTime, self.processes[self.numProcesses - 1].arrivalTime)
        self.x += [curr, lastTime]
        self.y += [0, 0]
        while len(self.finishList) < self.numProcesses:
            self.__fillQueue(queue, lastTime)
            process = queue.pop()
            if process.arrivalTime > lastTime:
                self.x += [lastTime, process.arrivalTime]
                self.y += [0, 0]
                lastTime = process.arrivalTime
            print("Process " + str(process.num) +
                  " begins at : " + str(lastTime))
            execTime = min(self.rrQuantum, process.remaining)
            process.remaining -= execTime
            process.waitingTime += lastTime - process.last
            curr = lastTime
            lastTime += execTime
            self.x += [curr, lastTime]
            self.y += [process.num, process.num]
            process.last = lastTime
            if process.remaining <= 0:
                process.tat = process.last - process.arrivalTime
                process.weightedTAT = process.tat / process.burstTime
                self.finishList.append(process)
            # if remaining = 0 .. push and handle it in __fillQueue
            queue.insert(0, process)
            print("Process " + str(process.num) +
                  " stops at : " + str(lastTime))
            curr = lastTime
            lastTime += self.switchTime
            if self.switchTime != 0:
                self.x += [curr, lastTime]
                self.y += [0, 0]

    def SRTN(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))
        queue = self.processes.copy()
        queue.reverse()
        readyQueue = []
        curr = 0
        lastTime = self.switchTime
        self.x += [0, lastTime]
        self.y += [0, 0]

        while len(queue) > 0 or len(readyQueue) > 0:
            if len(readyQueue) == 0:
                process = queue.pop()
                if process.arrivalTime > lastTime:
                    self.x += [lastTime, process.arrivalTime]
                    self.y += [0, 0]
                    lastTime = process.arrivalTime
                readyQueue += [process]

            temp = []
            for x in queue:
                if x.arrivalTime <= lastTime:
                    readyQueue.append(x)
                    temp.append(x)
            for x in temp:
                queue.remove(x)

            readyQueue.sort(key=lambda x: (x.remaining, x.num))

            runningProcess = readyQueue[0]
            runningProcess.waitingTime += lastTime - runningProcess.last
            readyQueue.remove(runningProcess)

            if len(queue) > 0 and runningProcess.remaining + lastTime >= queue[len(queue) - 1].arrivalTime:
                curr = lastTime
                runningProcess.last = queue[len(queue) - 1].arrivalTime
                lastTime = queue[len(queue) - 1].arrivalTime
                runningProcess.remaining -= (lastTime - curr)

                self.x += [curr, lastTime]
                self.y += [runningProcess.num, runningProcess.num]

                if runningProcess.remaining != 0:
                    readyQueue.append(runningProcess)
                else:
                    runningProcess.tat = runningProcess.last - runningProcess.arrivalTime
                    runningProcess.weightedTAT = runningProcess.tat / runningProcess.burstTime
                    self.finishList.append(runningProcess)

                for x in queue:
                    if x.arrivalTime <= lastTime:
                        readyQueue.append(x)
                        queue.remove(x)
                readyQueue.sort(key=lambda x: (x.remaining, x.num))
                curr = lastTime
                lastTime += self.switchTime
                if self.switchTime != 0:
                    self.x += [curr, lastTime]
                    self.y += [0, 0]
                continue
            else:
                curr = lastTime
                lastTime += runningProcess.remaining
                runningProcess.last = lastTime
                runningProcess.tat = runningProcess.last - runningProcess.arrivalTime
                runningProcess.weightedTAT = runningProcess.tat / runningProcess.burstTime
                self.finishList.append(runningProcess)
                self.x += [curr, lastTime]
                self.y += [runningProcess.num, runningProcess.num]

                curr = lastTime
                lastTime += self.switchTime
                if self.switchTime != 0:
                    self.x += [curr, lastTime]
                    self.y += [0, 0]
                continue

    def SRTN2(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        lastTime = self.processes[0].arrivalTime
        queue = self.processes.copy()  # this queue holds all processes. After the execution of a process it is deleted from this queue.
        previousExecutingProcess = self.processes[0].num
        infinityRemainingProcess = Process(-1, 10000000, 0, 0)
        queue.append(infinityRemainingProcess)
        arrived = []
        tat = 0
        while len(queue) > 0 or len(arrived) > 0:
            arrived += [process for process in queue if process.arrivalTime <= lastTime]
            if len(arrived) == 0:
                if len(queue) == 1:
                    return

                self.x += [lastTime, lastTime + queue[0].arrivalTime]
                self.y += [0, 0]
                lastTime = queue[0].arrivalTime
                continue

            queue = [process for process in queue if process.arrivalTime > lastTime]
            # no need to initialize the remaining time it's already initialized in the constructor
            arrived.sort(key=lambda x: (x.remaining, x.num))  # Sort processes by remaining time
            curr = lastTime
            if arrived[0].remaining <= queue[0].arrivalTime - lastTime:
                switched = 0
                if arrived[0].num != previousExecutingProcess:
                    lastTime += self.switchTime
                    if self.switchTime != 0:
                        self.x += [lastTime - self.switchTime, lastTime]
                        self.y += [0, 0]
                        print("process num " + str(arrived[0].num) + " switched")
                        switched = 1
                    curr = lastTime

                lastTime += arrived[0].remaining
                tat = lastTime - arrived[0].arrivalTime
                self.processes[arrived[0].num - 1].tat = tat
                self.processes[arrived[0].num - 1].weightedTAT = tat / arrived[0].burstTime
                self.processes[arrived[0].num - 1].waitingTime = tat - arrived[0].burstTime
                self.finishList += [arrived[0]]  # another [] ??
                print("Process " + str(arrived[0].num) + " ends at : " + str(lastTime))
                self.x += [curr, lastTime]
                self.y += [arrived[0].num, arrived[0].num]
                previousExecutingProcess = arrived[0].num
                '''lastTime += self.switchTime
                if self.switchTime != 0:
                    self.x += [lastTime-self.switchTime, lastTime]
                    self.y += [0, 0]
                    print ("process num "+ str(arrived[0].num)+" switched")'''
                arrived.remove(arrived[0])
                # continue
            else:
                switched = 0
                if arrived[0].num != previousExecutingProcess:
                    lastTime += self.switchTime
                    if self.switchTime != 0:
                        self.x += [lastTime - self.switchTime, lastTime]
                        self.y += [0, 0]
                        print("process num " + str(arrived[0].num) + " switched")
                        switched = 1
                    curr = lastTime
                arrived[0].remaining -= queue[0].arrivalTime - lastTime
                lastTime = queue[0].arrivalTime
                if switched == 1:
                    self.x += [curr, lastTime + self.switchTime]
                    lastTime += self.switchTime
                else:
                    self.x += [curr, lastTime]
                self.y += [arrived[0].num, arrived[0].num]
                previousExecutingProcess = arrived[0].num

            if len(queue) == 1 and len(arrived) == 0:
                return

    def printInfo(self):
        TAT = 0
        WTAT = 0
        for process in self.finishList:
            print("Process {0}: wait={1}, tat ={2} , wTat={3}".format(process.num, process.waitingTime, process.tat,
                                                                      process.weightedTAT))
            TAT += process.tat
            WTAT += process.weightedTAT
        print("Avg TAT = {0}\nAvg WTAT = {1}".format(
            TAT / len(self.processes), WTAT / len(self.processes)))

    def drawGraph(self):
        plt.xlabel('time')
        plt.ylabel('process id')
        plt.title('Scheduling')
        plt.plot(self.x, self.y, 'b')
        # ax = plt.gca()
        # def f(x, pos): return str(x).rstrip('0').rstrip('.')
        # ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
        # ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(f))
        plt.show()
        print(self.x)
        print(self.y)


def main():
    scheduler = Scheduler([
        Process(1, 5, 3, 1),
        Process(2, 6, 8, 1),
        Process(3, 8, 9, 1),
    ], 2, 2)
    # scheduler = Scheduler(
    #     [
    #         Process(1, 4, 7, 1),
    #         Process(2, 5, 5, 2),
    #         Process(3, 6, 3, 3),
    #         Process(4, 7, 1, 5),
    #         Process(5, 8, 2, 4),
    #         Process(6, 9, 1, 4),
    #     ], 2, 2)
    scheduler.RR()
    scheduler.printInfo()
    scheduler.drawGraph()


if __name__ == '__main__':
    main()
