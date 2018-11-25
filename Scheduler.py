import numpy as np
from Process import *


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
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        queue = self.processes.copy()
        queue.reverse()
        lastTime = self.processes[0].arrivalTime
        while len(queue) > 0:
            process = queue.pop()
            if process.arrivalTime > lastTime:
                self.x += [lastTime, process.arrivalTime]
                self.y += [0, 0]
                lastTime = process.arrivalTime
            print("Process " + str(process.num) + " begins at : " + str(lastTime))
            process.waitingTime += lastTime - process.arrivalTime  # waiting = start - arrival
            process.status = 0
            curr = lastTime
            lastTime += process.burstTime
            self.x += [curr, lastTime]
            self.y += [process.num, process.num]
            process.tat += lastTime - process.arrivalTime  # turn around time = finish - arrival
            process.weightedTAT = process.tat / process.burstTime
            print("Process " + str(process.num) + " ends at : " + str(lastTime))
            self.finishList += [process]
            curr = lastTime
            lastTime += self.switchTime
            self.x += [curr, lastTime]
            self.y += [0, 0]

    def HPF(self): ##not tested or even compiled yet
            self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
            lastTime = self.processes[0].arrivalTime
            queue = self.processes.copy() # this queue holds all processes. After the execution of a process it is deleted from this queue.
            while len(queue)>0:
                hp = [process for process in queue if process.arrivalTime<=lastTime] #this list will hold the arrived processes, priority sorted
                if len(hp)==0:
                    lastTime=queue[0].arrivalTime
                    self.x+=[lastTime, queue[0].arrivalTime]
                    self.y+=[0,0]
                    continue
                hp.sort(key=lambda x: (x.priority, x.num))  # Sort processes by priority
                lastTime+=hp[0].burstTime
                self.finishList+=[hp[0]] # should i use another [] ??
                # here we should assign the tat to the process. ask mo2men
                tat=lastTime-hp[0].arrivalTime
                self.processes[hp[0].num-1].tat=tat
                self.processes[hp[0].num-1].weightedTAT=tat/hp[0].burstTime
                print("Process " + str(hp[0].num) + " ends at : " + str(lastTime))
                self.x+=[lastTime-hp[0].burstTime,lastTime]
                self.y+=[hp[0].num,hp[0].num]
                lastTime+=self.switchTime
                if self.switchTime != 0:
                    self.x += [lastTime-self.switchTime, lastTime]
                    self.y += [0, 0]
                queue.remove(hp[0])
                hp.remove(hp[0])

    def __fillQueue(self, queue, lastTime):
        # assumptions
        # 1 - if one process finishes its quantum and (one process or more y3ny) came at the end of execution .. i choose new first
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
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        self.visited = [False] * self.numProcesses
        self.finishList = []
        queue = []
        lastTime = self.processes[0].arrivalTime
        self.processes.reverse()
        while len(self.finishList) < self.numProcesses:
            self.__fillQueue(queue, lastTime)
            process = queue.pop()
            if process.arrivalTime > lastTime:
                self.x += [lastTime, process.arrivalTime]
                self.y += [0, 0]
                lastTime = process.arrivalTime
            print("Process " + str(process.num) + " begins at : " + str(lastTime))
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
            print("Process " + str(process.num) + " stops at : " + str(lastTime))
            curr = lastTime
            lastTime += self.switchTime
            if self.switchTime != 0:
                self.x += [curr, lastTime]
                self.y += [0, 0]

    def SRTN(self):
        self.processes.sort(key=lambda x: (x.arrivalTime, x.num))  # Sort by a Custom Property
        lastTime = self.processes[0].arrivalTime
        queue = self.processes.copy() # this queue holds all processes. After the execution of a process it is deleted from this queue.
        previousExecutingProcess = self.processes[0].num
        infinityRemainingProcess= Process(-1,10000000,0,0)
        queue.append(infinityRemainingProcess)
        arrived=[]
        tat=0
        while len(queue)>0 or len(arrived)>0:
            arrived += [process for process in queue if process.arrivalTime<=lastTime]
            if len(arrived)==0:
                if len(queue)==1:
                    return
                
                self.x+=[lastTime,lastTime+queue[0].arrivalTime]
                self.y+=[0,0]
                lastTime=queue[0].arrivalTime
                continue

            queue=[process for process in queue if process.arrivalTime>lastTime]
            #no need to initialize the remaining time it's already initialized in the constructor
            arrived.sort(key=lambda x: (x.remaining, x.num))  # Sort processes by remaining time
            curr=lastTime
            if arrived[0].remaining<=queue[0].arrivalTime-lastTime :
                lastTime+=arrived[0].remaining
                tat=lastTime-arrived[0].arrivalTime 
                self.processes[arrived[0].num-1].tat=tat
                self.processes[arrived[0].num-1].weightedTAT=tat/arrived[0].burstTime
                self.processes[arrived[0].num-1].waitingTime=tat-arrived[0].burstTime
                self.finishList+= [arrived[0]] # another [] ??
                print("Process " + str(arrived[0].num) + " ends at : " + str(lastTime))
                self.x+=[curr,lastTime]
                self.y+=[arrived[0].num,arrived[0].num]
                previousExecutingProcess=arrived[0].num
                lastTime += self.switchTime
                if self.switchTime != 0:
                    self.x += [lastTime-self.switchTime, lastTime]
                    self.y += [0, 0]
                    print ("process num "+ str(arrived[0].num)+" switched")
                arrived.remove(arrived[0])
                #continue
            else:
                if arrived[0].num !=previousExecutingProcess:
                    lastTime += self.switchTime
                    if self.switchTime != 0:
                        self.x += [lastTime-self.switchTime, lastTime]
                        self.y += [0, 0]
                        print ("process num "+ str(arrived[0].num)+" switched")
                    curr=lastTime
                arrived[0].remaining-=queue[0].arrivalTime-lastTime
                lastTime=queue[0].arrivalTime
                self.x+=[curr,lastTime]
                self.y+=[arrived[0].num,arrived[0].num]
                previousExecutingProcess=arrived[0].num


            if len(queue)==1 and len(arrived)==0:
                return

	
    def printInfo(self):
        TAT = 0
        WTAT = 0
        for process in self.finishList:
            print("Process {0}: wait={1}, tat ={2} , wTat={3}".format(process.num, process.waitingTime, process.tat,
                                                                      process.weightedTAT))
            TAT += process.tat
            WTAT += process.weightedTAT
        print("Avg TAT = {0}\nAvg WTAT = {1}".format(TAT / len(self.processes), WTAT / len(self.processes)))

    def drawGraph(self):
        plt.xlabel('time')
        plt.ylabel('process id')
        plt.title('Scheduling')
        plt.plot(self.x, self.y, 'b')
        #ax = plt.gca()
        #f = lambda x, pos: str(x).rstrip('0').rstrip('.')
        #ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
        #ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(f))
        plt.show()
        print(self.x)
        print(self.y)


def main():
    scheduler = Scheduler(
        [
            Process(1, 0, 7, 1),
            Process(2, 1, 5, 2),
            Process(3, 2, 3, 3),
            Process(4, 3, 1, 5),
            Process(5, 4, 2, 4),
            Process(6, 5, 1, 4),
        ], 1, 2)


    scheduler.SRTN()
    scheduler.printInfo()
    #scheduler.drawGraph()


if __name__ == '__main__':
    main()
