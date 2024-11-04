import struct
import sys
import numpy as np
from numpy import polyfit


struct_fmt = 'QQQ4qI3900s'
struct_len = struct.calcsize(struct_fmt)
struct_unpack = struct.Struct(struct_fmt).unpack_from

if (len(sys.argv) < 3):
    print("Error no enough argument")
    sys.exit(0)


targetChannel = int(sys.argv[2])

orinGap = 0

# This piece of code is to analyze whether there is data is not send by esp32

# for stripId in range(4):

fileName = f'{sys.argv[1]}'
f = open(fileName, "rb")
structNum = 0
preCurrent = 0
preList = [0] * 350
isFirst = True
targetTime = 0
while True:
    data = f.read(struct_len)
    if not data:
        break
    structNum = structNum + 1
    s = struct_unpack(data)

    frameLen = s[7] / 12
    # print(frameLen)
    timeStamp = int(s[0] / 256)
    
    for j in range(int(frameLen)):
        index = j * 12 + targetChannel * 3
        tempCurrent = -10
        if s[8][index] >= 128:
            tempCurrent = -16777216
        else:
            tempCurrent = 0
        tempCurrent |= (int(s[8][index]) << 16)
        tempCurrent |= (int(s[8][index + 1]) << 8)
        tempCurrent |= (int(s[8][index + 2]))
        if isFirst:
            preList[j] = tempCurrent
        if targetTime < timeStamp and(tempCurrent > preList[j] + 20000 or tempCurrent < preList[j] - 20000):
            # print(f"Gap\t{s[0]/256}\t{structNum}\t{j}", end='\t')
            targetTime = timeStamp + 1700000
            preCurrent = 0

            maxVolt = -1000
            minVolt = 10000000
            crsPoint = 0
            preVolt = -1
            voltList = []
            # print(timeStamp)
            for l in range(int(frameLen)):
                index = l * 12 + 9
                # for l in range(8):
                tempCurrent = -10
                if s[8][index] >= 128:
                    tempCurrent = -16777216
                else:
                    tempCurrent = 0
                tempCurrent |= (int(s[8][index]) << 16)
                tempCurrent |= (int(s[8][index + 1]) << 8)
                tempCurrent |= (int(s[8][index + 2]))
                voltList.append(tempCurrent)
                if tempCurrent < minVolt:
                    minVolt = tempCurrent
                if tempCurrent > maxVolt:
                    maxVolt = tempCurrent
                if preVolt >= 0 and tempCurrent < 0:
                    crsPoint = l - 1
                preVolt = tempCurrent
            #     print(tempCurrent)
            # print(voltList[crsPoint - 5:crsPoint + 25])
            npVoltList = np.array(voltList)
            npx = np.arange(1, 31)
            coeff = polyfit(npx, npVoltList[crsPoint - 5:crsPoint + 25], 1)
            crsX = ((0) / 2 - coeff[1]) / coeff[0]
            crsX = crsX + crsPoint - 6
            print(f"{timeStamp}\t{j}\t{j - crsX}")
            # print(f"{timeStamp}\t{j}\t{j - crsX}\t{(maxVolt + minVolt)}\t{crsX}")

            # if crsX < 159 or crsX >= 161:
            #     print((maxVolt + minVolt) / 2,
            #           crsPoint, crsX, len(voltList))

        preList[j] = tempCurrent
    if isFirst:
        isFirst = False
