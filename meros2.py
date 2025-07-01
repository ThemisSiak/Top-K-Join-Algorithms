#Siakavara Themistokleia, 4786
import sys
import heapq
import time

def getImportantFields(fields):
    recordID = int(fields[0])
    age = int(fields[1])
    instanceWeight = float(fields[25])
    return (recordID, age, instanceWeight)

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

def getTimeB(startTime, endTime):
    return endTime-startTime

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python program.py K")
        sys.exit(1)

    startTime = time.time()
    K = int(sys.argv[1])
    with open('males_sorted', 'r') as malesFile, open('females_sorted', 'r') as femalesFile:
        minHeap = topKjoinB(malesFile, femalesFile, K)
        print(f"Top-{K} pairs:")
        for idx, (score, pair) in enumerate(minHeap, start=1):
            print(f"{idx}. pair: {pair} score: {score:.2f}")
    endTime = time.time()

    print(f"Runtime: {endTime - startTime: .4f} seconds")
