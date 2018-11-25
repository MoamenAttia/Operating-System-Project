class Process:
    def __init__(self, num=0, arrivalTime=0, burstTime=0, priority=0):
        self.num = num
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remaining = burstTime
        self.last = arrivalTime
        self.priority = priority
        self.status = 1  # 1 means active 0 means not active
        self.tat = 0
        self.waitingTime = 0
        self.weightedTAT = 0


def main():
    p = Process()
    print(vars(p))


if __name__ == '__main__':
    main()
