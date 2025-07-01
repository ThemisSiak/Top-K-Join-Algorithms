#Siakavara Themistokleia, 4786
import matplotlib.pyplot as plt

import sys
import heapq
import time

def getImportantFields(fields):
    recordID = int(fields[0])
    age = int(fields[1])
    instanceWeight = float(fields[25])
    return (recordID, age, instanceWeight)

def writeMalesData(malesFile):
    global p1_max
    global p1_cur
    global validLinesMale

    malesLine = malesFile.readline().strip().split(',')
    if len(malesLine) < 2:
        if 0 not in males:
            males[0] = []
        males[0].append(())
        return None, p1_max, p1_cur, validLinesMale
    if not malesLine[8].startswith(" Married") and int(malesLine[1])>=18:
        validLinesMale +=1
        p1_cur = float(malesLine[25])
        if len(males)==0:
            p1_max = p1_cur
        malesRecord = getImportantFields(malesLine)
        if malesRecord[1] not in males:
            males[malesRecord[1]] = []
        males[malesRecord[1]].append((malesRecord[0], malesRecord[2]))
        return malesRecord, p1_max, p1_cur, validLinesMale
    else:
        return writeMalesData(malesFile)

def writeFemalesData(femalesFile):
    global p2_max
    global validLinesFemale

    femalesLine = femalesFile.readline().strip().split(',')
    if len(femalesLine) < 2:
        return None, p2_max, p2_cur, validLinesFemale
    if not femalesLine[8].startswith(" Married") and int(femalesLine[1])>=18:
        validLinesFemale+=1
        p2_cur = float(femalesLine[25])
        if len(females)==0:
            p2_max = p2_cur
        femalesRecord = getImportantFields(femalesLine)
        if femalesRecord[1] not in females:
            females[femalesRecord[1]] = []
        females[femalesRecord[1]].append((femalesRecord[0], femalesRecord[2]))
        return femalesRecord, p2_max, p2_cur, validLinesFemale
    else:
        return writeFemalesData(femalesFile)

def topKjoin(malesFile, femalesFile):
    global males
    global females
    global p1_max, p1_cur, p2_max, p2_cur
    global T
    global Q
    global validLinesMale
    global validLinesFemale

    totalWeight = 0

    while True:
        if len(males)==0:
            malesRecord, p1_max, p1_cur, validLinesMale = writeMalesData(malesFile)
            femalesRecord, p2_max, p2_cur, validLinesFemale = writeFemalesData(femalesFile)
            T = max(p1_max + p2_cur, p1_cur + p2_max)

            if malesRecord[1] == femalesRecord[1]:
                totalWeight = malesRecord[2] + femalesRecord[2]
                if totalWeight>=T:
                    heapq.heappush(Q, (totalWeight, (malesRecord[0], femalesRecord[0])))
        elif len(males) == len(females):
            malesRecord, p1_max, p1_cur, validLinesMale = writeMalesData(malesFile)
            if malesRecord == None:
                continue
            T = max(p1_max + p2_cur, p1_cur + p2_max)

            for woman in females.get(malesRecord[1], []):
                totalWeight = malesRecord[2] + woman[1]
                if totalWeight >= T:
                    heapq.heappush(Q, (totalWeight, (malesRecord[0], woman[0])))
        else:
            femalesRecord, p2_max, p2_cur, validLinesFemale = writeFemalesData(femalesFile)
            if femalesRecord == None:
                break
            T = max(p1_max + p2_cur, p1_cur + p2_max)

            for man in males.get(femalesRecord[1], []):
                totalWeight = femalesRecord[2] + man[1]
                if totalWeight >= T:
                    heapq.heappush(Q, (totalWeight, (man[0], femalesRecord[0])))
        while Q and Q[0][0]>= T:
            topElement = heapq.heappop(Q)
            yield topElement[1], topElement[0]

def algorithmA(K):
    global Q
    global T
    global p1_max, p1_cur, p2_max, p2_cur
    global males
    global females
    global validLinesMale
    global validLinesFemale
    
    startTime = time.time()
    with open('males_sorted', 'r') as malesFile, open('females_sorted', 'r') as femalesFile:
       Q = []
       T = 0
       p1_max, p1_cur, p2_max, p2_cur = 0, 0, 0, 0
       males = {}
       females = {}
       validLinesMale=0
       validLinesFemale=0

       result = topKjoin(malesFile, femalesFile)
       print(f"Top-{K} pairs:")
       idx=1
       for count in range(0,K):
           joinR = next(result)
           print(f"{idx}. pair: {joinR[0]} score: {joinR[1]:.2f}")
           idx +=1
    endTime = time.time()

    print(f"Runtime: {endTime - startTime: .4f} seconds")
    return endTime - startTime, validLinesMale, validLinesFemale

def readMalesFile(malesFile):
    males = {}
    malesLine = malesFile.readline().strip().split(',')
    while len(malesLine)>1:
        if not malesLine[8].startswith(" Married") and int(malesLine[1])>=18:
            malesRecord = getImportantFields(malesLine)
            if malesRecord[1] not in males:
                males[malesRecord[1]] = []
            males[malesRecord[1]].append((malesRecord[0], malesRecord[2]))
        malesLine = malesFile.readline().strip().split(',')
    return males

def topKjoinB(malesFile, femalesFile, K):
    males = readMalesFile(malesFile)
    minHeap = []

    for line in femalesFile:
        fields = line.strip().split(',')
        if not fields[8].startswith(" Married") and int(fields[1]) >=18:
            femaleRecord = getImportantFields(fields)
            age = femaleRecord[1]
            if age in males:
                for maleRecord in males[age]:
                    totalWeight = maleRecord[1] + femaleRecord[2]
                    if len(minHeap)<K:
                        heapq.heappush(minHeap, (totalWeight, (maleRecord[0], femaleRecord[0])))
                    else:
                        if totalWeight > minHeap[0][0]:
                            heapq.heappushpop(minHeap, (totalWeight, (maleRecord[0], femaleRecord[0])))
    minHeap.sort(reverse=True, key=lambda x: x[0])
    return minHeap

def algorithmB(K):
    startTime = time.time()
    with open('males_sorted', 'r') as malesFile, open('females_sorted', 'r') as femalesFile:
        minHeap = topKjoinB(malesFile, femalesFile, K)
        print(f"Top-{K} pairs:")
        for idx, (score, pair) in enumerate(minHeap, start=1):
            print(f"{idx}. pair: {pair} score: {score:.2f}")
    endTime = time.time()

    print(f"Runtime: {endTime - startTime: .4f} seconds")
    return endTime - startTime

if __name__ == "__main__":
    Kvalues = [1,2,5,10,20,50,100]
    timeValues = [1,10,100,1000,10000]

    totalTimesA = []
    totalTimesB = []

    for K in Kvalues:
        timeA, validM, validF = algorithmA(K)
        totalTimesA.append(timeA *1000)
        print("K=", K, ":Valid lines in Males:", validM, "-Females:", validF)

        timeB = algorithmB(K)
        totalTimesB.append(timeB *1000)


    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(Kvalues, totalTimesA, label='Algorithm A', marker='o')
    plt.plot(Kvalues, totalTimesB, label='Algorithm B', marker='s')
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(Kvalues, [str(k) for k in Kvalues])
    plt.yticks(timeValues, [str(t) for t in timeValues])
    plt.xlabel('K')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Execution Time of Top-K Join Algorithms')
    plt.legend()

    plt.savefig('topKjoin_comparison.png')
            
