import sys
import numpy as np

if len(sys.argv) < 3:
    print(f"Error!\t Usage: python ./StatErr.py outputFile1 outputFile2")

file_path = sys.argv[1]
data1 = []

with open(file_path, 'r') as file:
    for line in file:
        columns = line.strip().split('\t')
        if len(columns) == 3:
            try:
                int_value = int(columns[0])
                int_val2 = int(columns[1])
                float_value = float(columns[2])
                data1.append([int_value, int_val2, float_value])
            except ValueError:
                print(f"Ignoring line: {line.strip()} (Invalid data)")
        else:
            print(f"Ignoring line: {line.strip()} (Expected 2 columns)")

file_path = sys.argv[2]
data2 = []

with open(file_path, 'r') as file:
    for line in file:
        columns = line.strip().split('\t')
        if len(columns) == 3:
            try:
                int_value = int(columns[0])
                int_val2 = int(columns[1])
                float_value = float(columns[2])
                data2.append([int_value, int_val2, float_value])
            except ValueError:
                print(f"Ignoring line: {line.strip()} (Invalid data)")
        else:
            print(f"Ignoring line: {line.strip()} (Expected 2 columns)")


ind1 = 0
ind2 = 0

FinalSyncError = []

while True:
    if ind1 >= len(data1) or ind2 >= len(data2):
        break

    if data1[ind1][0] - data2[ind2][0] > -1000 and data1[ind1][0] - data2[ind2][0] < 1000:
        if ((data1[ind1][1] > 5 and data1[ind1][1] <= 155) or (data1[ind1][1] > 165 and data1[ind1][1] < 315)):
            FinalSyncError.append(data2[ind2][2] - data1[ind1][2] -
                                  (data2[ind2][1] - data1[ind1][1]))
        ind1 += 1
        ind2 += 1
    elif data1[ind1][0] - data2[ind2][0] <= -1000:
        ind1 += 1
    elif data1[ind1][0] - data2[ind2][0] >= 1000:
        ind2 += 1

AbsSyncErr = np.abs(FinalSyncError)
maxAbsSyncErr = np.max(AbsSyncErr)

print(f'Totaling of {len(AbsSyncErr)} samples.')

print(f"Max sync error is {maxAbsSyncErr} times of sampling interval.")

print(f"Max sync error is {maxAbsSyncErr * 62.5} us.")

with open('./Result/syncErrList.txt', 'w+') as outFile:
    for sync in AbsSyncErr:
        outFile.write(f"{sync}\n")
