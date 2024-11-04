# This file is used to train the model
import numpy as np
from numpy import fft
from sklearn.metrics import accuracy_score, classification_report
import time
import xgboost
import os

RemainLen = 10

if __name__ == '__main__':
    # This part shows mappings between BLUED appliance type with our internal index.
    eventName = {111:0, 127:1, 156:2, 158:3, 147:4, 108:5, 132:6, 148:7}
    
    # 111.Fridge
    # 127.Air	Compressor
    # 156.Bathroom	upstairs	lights
    # 158.Bedroom	Lights
    # 147.Backyard	lights
    # 108.Kitchen	Aid	Chopper
    # 132.Hair	Dryer
    # 148.Washroom	light

    # BLUED dataset has many multi-state appliances and here stores how many events corresponding to the appliance.
    lineLen = [8, 2, 4, 2, 2, 6, 2, 2]
    
    appNameList = ["Fridge", "Air Compressor", "Bathroom upstairs lights", "Bedroom Lights", "Backyard lights", "Kitchen Aid Chopper", "Hair Dryer", "Washroom light"]
    
    
    idRange = [8, 10, 14, 16, 18, 24, 26, 28]
    preTimeStamp = 0.0
    
    predictResults = [[] for _ in range(8)]
    
    model = xgboost.XGBClassifier()
    model.load_model("./XGBoost-Best-Final.model")

    preOff = -1
    
    fileCont = np.load(f'./event.npz', allow_pickle=True)
    sumCurList = fileCont['Data'].reshape((-1, 200))
    tagList = fileCont['Tag']
    eventIdList = fileCont['EventIdList']
    
    
    tpCount = [0] * 9
    fpCount = [0] * 9
    fnCount = [0] * 9
    
    testDat_fft = fft.fft(sumCurList)[:, :RemainLen] / 101

    testFFTDat = np.concatenate(
        (np.abs(testDat_fft), np.imag(testDat_fft), np.real(testDat_fft), np.imag(testDat_fft[:,1:2]), np.imag(testDat_fft[:,1:2])), axis=1)

    # This is a trick, we train and test with this transform
    # # testFFTDat[RemainLen] *= 1000
    testFFTDat[:, 0] = testFFTDat[:, 0] + testFFTDat[:, 1]
    testFFTDat[:, RemainLen] += testFFTDat[:, RemainLen + 1]
    testFFTDat[:, RemainLen*2] += testFFTDat[:, RemainLen*2 + 1]
    # fftCheck = np.abs( testFFTDat[:, RemainLen + 1])
    Test_Xs = testFFTDat
    
    startTime = time.time()
    EventList = [[] for i in range(8)]
    
    testOut = model.predict(Test_Xs)
    print("Prediction time: ", time.time() - startTime)
    
    for i in range(0, len(testOut)// 30):
        counts = np.bincount(testOut[i*30:i*30+30])
        if len(counts) > 7:
            if counts[7] > 8:
                for j in range(7):
                    counts[j] = 0
        maxPos = np.argmax(counts)
        
        for l in range(8):
            if maxPos < idRange[l]:
                maxPos = l
                break
        
        if tagList[i] == maxPos:
            tpCount[maxPos] += 1
        else:
            # for j in range(30):
            #     print(Test_Xs[i*30+j][RemainLen + 1], end = '\t')
            fpCount[maxPos] += 1
            fnCount[tagList[i]] += 1
    
    f1List = []
    
    for i in range(8):
        precision = tpCount[i] / (tpCount[i] + fpCount[i])
        recall = tpCount[i] / (tpCount[i] + fnCount[i])
        f1Score = 2 * precision * recall / (precision + recall)
        f1List.append(f1Score)
        print(appNameList[i], precision, recall, f1Score, sep = '\t')
    avgF = np.average(f1List)
    print("Average F1 score: ", avgF)
    