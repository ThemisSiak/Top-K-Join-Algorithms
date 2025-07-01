#Siakavara Themistokleia, 4786
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

    malesLine = malesFile.readline().strip().split(',')
    if len(malesLine) < 2:
        if 0 not in males:
            males[0] = []
        males[0].append(())
        return None, p1_max, p1_cur
    if not malesLine[8].startswith(" Married") and int(malesLine[1])>=18:
        p1_cur = float(malesLine[25])
        if len(males)==0:
            p1_max = p1_cur
        malesRecord = getImportantFields(malesLine)
        if malesRecord[1] not in males:
            males[malesRecord[1]] = []
        males[malesRecord[1]].append((malesRecord[0], malesRecord[2]))
        return malesRecord, p1_max, p1_cur
    else:
        return writeMalesData(malesFile)

def writeFemalesData(femalesFile):
    global p2_max

    femalesLine = femalesFile.readline().strip().split(',')
    if len(femalesLine) < 2:
        return None, p2_max, p2_cur
    if not femalesLine[8].startswith(" Married") and int(femalesLine[1])>=18:
        p2_cur = float(femalesLine[25])
        if len(females)==0:
            p2_max = p2_cur
        femalesRecord = getImportantFields(femalesLine)
        if femalesRecord[1] not in females:
            females[femalesRecord[1]] = []
        females[femalesRecord[1]].append((femalesRecord[0], femalesRecord[2]))
        return femalesRecord, p2_max, p2_cur
    else:
        return writeFemalesData(femalesFile)

def topKjoin(malesFile, femalesFile):
    global males
    global females
    global p1_max, p1_cur, p2_max, p2_cur
    global T
    global Q

    totalWeight = 0

    while True:
        if len(males)==0:
            malesRecord, p1_max, p1_cur = writeMalesData(malesFile)
            femalesRecord, p2_max, p2_cur = writeFemalesData(femalesFile)
            T = max(p1_max + p2_cur, p1_cur + p2_max)

            if malesRecord[1] == femalesRecord[1]:
                totalWeight = malesRecord[2] + femalesRecord[2]
                if totalWeight>=T:
                    heapq.heappush(Q, (totalWeight, (malesRecord[0], femalesRecord[0])))
        elif len(males) == len(females):
            malesRecord, p1_max, p1_cur = writeMalesData(malesFile)
            if malesRecord == None:
                continue
            T = max(p1_max + p2_cur, p1_cur + p2_max)
 
            for woman in females.get(malesRecord[1], []):
                totalWeight = malesRecord[2] + woman[1]
                if totalWeight >= T:
                    heapq.heappush(Q, (totalWeight, (malesRecord[0], woman[0])))
        else:
            femalesRecord, p2_max, p2_cur = writeFemalesData(femalesFile)
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

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python program.py K")
        sys.exit(1)

    K = int(sys.argv[1])

    startTime = time.time()
    with open('males_sorted', 'r') as malesFile, open('females_sorted', 'r') as femalesFile:
       Q = []
       T = 0
       p1_max, p1_cur, p2_max, p2_cur = 0, 0, 0, 0
       males = {}
       females = {}

       result = topKjoin(malesFile, femalesFile)
       print(f"Top-{K} pairs:")
       idx=1
       for count in range(0,K):
           joinR = next(result)
           print(f"{idx}. pair: {joinR[0]} score: {joinR[1]:.2f}")
           idx +=1
    endTime = time.time()

    print(f"Runtime: {endTime - startTime: .4f} seconds")
            
