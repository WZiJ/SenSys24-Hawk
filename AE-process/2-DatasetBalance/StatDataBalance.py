import numpy as np
import re
import sys

if len(sys.argv) < 2:
    print(f"Usage : python ./{sys.argv[0]} [Path to HawkDATA's file]")
    exit(-1)

hawkPath = sys.argv[1]

trainEventCount = [0] * 18
trainOnStateList = [0] * 18
trainOffStateList = [0] * 18

# Combine event ground truth for event balance evaluation
for fileId in range(30):
    fileCont = open(f'../../EventGroundTruth/Train/OpenList{fileId}.txt')
    fLines = fileCont.readlines()
    for appId in range(18):
        lineConts = fLines[appId + 1].split(':')
        appName = lineConts[0]
        eventList = re.findall("\d+",lineConts[1])
        eventPos = [int(jd) for jd in eventList]
        if len(eventPos) > 1:
            trainEventCount[appId] += len(eventPos)

for fileId in range(18):
    fileCont = open(f'../../EventGroundTruth/Test/FeaList{fileId}.txt')
    fLines = fileCont.readlines()
    for appId in range(18):
        lineConts = fLines[appId].split(':')
        appName = lineConts[0]
        eventList = re.findall("\d+",lineConts[1])
        eventPos = [int(jd) for jd in eventList]
        if len(eventPos) > 1:
            trainEventCount[appId] += len(eventPos)


# Combine state annotation for list

for fileId in range(30):
    fileCont = np.load(
        f'{hawkPath}/Train{fileId}.npz', allow_pickle=True)
    if fileId == 0:
        appNameList = fileCont['AppNameList']
    stateList = fileCont['StateList']
    totalNum = len(stateList[0])
    for i in range(18):
        onNum = np.sum(stateList[i])
        trainOnStateList[i] += onNum
        trainOffStateList[i] += totalNum - onNum
for fileId in range(18):
    fileCont = np.load(
        f'{hawkPath}/Test{fileId}.npz', allow_pickle=True)
    if fileId == 0:
        appNameList = fileCont['AppNameList']
    stateList = fileCont['StateList']
    totalNum = len(stateList[0])
    for i in range(18):
        onNum = np.sum(stateList[i])
        trainOnStateList[i] += onNum
        trainOffStateList[i] += totalNum - onNum

stateRadio = []

for i in range(18):
    minVal = min(trainOffStateList[i], trainOnStateList[i])
    maxVal = max(trainOffStateList[i], trainOnStateList[i])
    stateRadio.append(minVal / maxVal)
    
print("Event category BR is", np.min(trainEventCount)/ np.max(trainEventCount))
print("State ON category BR is", np.min(trainOnStateList) / np.max(trainOnStateList))
print("State average ON-OFF BR is", np.average(stateRadio))