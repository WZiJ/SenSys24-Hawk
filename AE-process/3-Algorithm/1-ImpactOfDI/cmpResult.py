import re
import sys
import numpy as np
def Merge(real, pred, endCycle):
    truePos = 0
    falsePos = 0
    falseNeg = 0
    if len(real) > 0:
        if real[0] < 100:
            real = real[1:]
    if len(real) > 0:
        if real[-1] > endCycle - 500:
            real = real[:-1]

    i = 0
    j = 0
    if len(real) > 1 and len(pred) > 1:
        if real[i] < 100:
            i += 1
        if pred[j] < 100:
            j += 1
        if real[-1] > endCycle - 500:
            real = real[:-1]
        if pred[-1] > endCycle - 500:
            pred = pred[:-1]
    while i < len(real) and j < len(pred):
        if real[i] < pred[j] - 1500:
            i += 1
            falseNeg += 1
        elif real[i] > pred[j] + 1500:
            j += 1
            falsePos += 1
        else:
            i += 1
            j += 1
            truePos += 1
    if i < len(real):
        falseNeg += len(real) - i
    if j < len(pred):
        falsePos += len(pred) - j
    return [truePos, falsePos, falseNeg]


lowAppNameList = ['Monitor', 'Humidifier',
                  'LEDLamp24w', 'LEDLamp36w', 'FluorescentLamp', 'Desktop', 'PhoneCharger', 'SweepingRobot']


appNameList = []

if __name__ == '__main__':
    endCycles = [70202, 72366, 76851, 157458, 149298, 151024, 158276, 148273, 150036, 156933, 149880, 146982, 155077, 148468, 145748, 157729, 148609, 146148]
    for diffGap in [2, 6, 10, 16, 20, 30, 40, 50]:
        truePos = [0] * 18
        falsePos = [0] * 18
        falseNeg = [0] * 18
        f1List = []
        accList = []
        oFile = open(f'./Result/XGBoost-{diffGap}.txt', 'w')
        for cmpIndx in range(18):
            endCycle = endCycles[cmpIndx]

            resultFile = open(f'../../../EventGroundTruth/Test/FeaList{cmpIndx}.txt', 'r')

            leftAllBuf = []
            rightAllBuf = []
            appNameList = []

            for i in range(18):
                line = resultFile.readline()
                lineConts = line.split(":")
                appNameList.append(lineConts[0])
                leftBuf = []
                rightBuf = []

                if len(lineConts) > 1:
                    numbers = re.findall('\d+', lineConts[1])
                    # print(numbers)
                    for l in range(0, len(numbers), 2):
                        lf = int(numbers[l])
                        rt = int(numbers[l + 1])
                        if rt > lf:
                            leftBuf.append(lf)
                            rightBuf.append(rt)
                if lineConts[0] in lowAppNameList and len(leftBuf) > 0 and leftBuf[0] == 0:
                    leftBuf = leftBuf[1:]
                    rightBuf = rightBuf[:-1]
                leftAllBuf.append(leftBuf)
                rightAllBuf.append(rightBuf)

            resultFile.close()

            fileLen = []

            highAppFile = open(f'./Result/Test-{diffGap}-{cmpIndx}.txt', 'r')

            fileConts = highAppFile.readlines()[1:]

            fileLen.append(endCycle)
            highAppFile.close()

            
            for l in range(0, 36, 2):
                startStr = re.findall('\d+', fileConts[l])
                endStr = re.findall('\d+', fileConts[l+1])
                
                
                appName = fileConts[l].split(' [')[0]
                # print(cmpIndx, appName)
                if appName == 'LEDLamp24w' or appName == 'LEDLamp36w':
                    startStr = startStr[1:]
                    endStr = endStr[1:]
                # print(startStr, endStr, leftAllBuf, rightAllBuf)
                if len(startStr) == 0 and len(endStr) == 0:
                    continue
                # print(cmpIndx, appName)
                startEvent = []
                endEvent = []
                for i in range(0, len(startStr)):
                    startEvent.append(int(startStr[i]))
                for i in range(0, len(endStr)):
                    endEvent.append(int(endStr[i]))

                for k in range(len(appNameList)):
                    if appNameList[k] == appName:
                        item = Merge(leftAllBuf[k], startEvent, endCycle)
                        item2 = Merge(rightAllBuf[k], endEvent, endCycle)
                        # print(cmpIndx, appName, startEvent, endEvent, endCycle, leftAllBuf[k], rightAllBuf[k], item, item2)

                        truePos[k] += item[0]+item2[0]
                        falsePos[k] += item[1]+item2[1]
                        falseNeg[k] += item[2]+item2[2]
                        # if appName == 'Desktop':
                        #     print(f'{cmpIndx} {item[0]} {item[1]} {item[2]} {item2[0]} {item2[1]} {item2[2]}')
                        break
        print('\nApp Name', 'True Pos', 'False Pos', 'False Neg','Recall','Precision','f1-score' ,sep='\t', file = oFile)
        for i in range(18):
            recall = truePos[i] / (truePos[i] + falseNeg[i])
            prec = truePos[i] / (truePos[i] + falsePos[i])
            f1score = 2 * recall * prec / (recall + prec)
            f1List.append(f1score)
            print(appNameList[i], truePos[i], falsePos[i], falseNeg[i], recall, prec, f1score, sep='\t', file=oFile)
        print(np.average(f1List), end='\t')
        print("Average F1 score:", np.average(f1List), file=oFile)
    print()