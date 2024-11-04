# This file is used to train the model
import numpy as np
from numpy import fft
import time
import xgboost
import sys

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} [Path to HawkDATA's file]")
    exit(-1)

basePath = sys.argv[1]

NormalVal = 26214
RemainLen = 10

if __name__ == '__main__':
    gapList = [2, 6, 10, 16, 20, 30, 40, 50]
    gapLen = len(gapList)

    testCurrent = []
    appNameList = []
    testLabel = [np.array([]) for _ in range(18)]
    thresHold = []
    for threFile in ['ISDiffXThres.txt']:
        thFile = open(f'../../../Models/{threFile}')
        thrLine = thFile.readline().split(',')
        print(len(thrLine))
        for i in range(36):
            thresHold.append(int(thrLine[i]))
    xgClass = xgboost.XGBClassifier()
    xgClass.load_model("../../../Models/ImbXGBoost.model")

    for fileId in range(18):
        fileCont = np.load(f'{basePath}/Test{fileId}.npz', allow_pickle=True)

        sumCurList = fileCont['MainMeterCurrent']
        appNameList = fileCont['AppNameList']
        diffGap = 30
        subCurList = np.divide(np.subtract(
            sumCurList[diffGap:], sumCurList[:-diffGap]), NormalVal)

        testDat_fft = fft.fft(subCurList)[:, :RemainLen] / 161
        testFFTDat = np.concatenate(
            (np.abs(testDat_fft), np.imag(testDat_fft), np.real(testDat_fft)), axis=1)
        testFFTDat[:, 0] = testFFTDat[:, 0] + testFFTDat[:, 1]
        testFFTDat[:, RemainLen] += testFFTDat[:, RemainLen + 1]
        testFFTDat[:, RemainLen*2] += testFFTDat[:, RemainLen*2 + 1]

        oFile = open(f'./Result/Test-{diffGap}-{fileId}.txt', 'w+')
        print(f'Gap {diffGap} for file {fileId}')
        startTime = time.time()
        EventList = [[] for _ in range(36)]
        testOut = xgClass.predict(testFFTDat)
        print("Prediction time: ", time.time() - startTime, file=oFile)

        for i in range(len(testOut)):
            if testOut[i] != 36:
                EventList[testOut[i]].append(i)

        reportEventList = [[] for _ in range(36)]

        for i in range(36):
            curInd = 0
            for k in range(len(EventList[i]) - thresHold[i] - 1):
                if k >= curInd:
                    if EventList[i][k] > EventList[i][k + thresHold[i]] - diffGap:
                        if len(reportEventList[i]) == 0 or reportEventList[i][-1] < EventList[i][k] - 50:
                            reportEventList[i].append(EventList[i][k])
                            curInd = thresHold[i] + k
        for i in range(36):
            print(appNameList[i // 2], reportEventList[i], file=oFile)
