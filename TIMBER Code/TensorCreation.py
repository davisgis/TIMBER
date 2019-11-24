import numpy as np
#For use to save and import the 3D matrix added on 10/27/2018. Source below
import pickle
from SupervisedAddition import *
#Adding this so that we can assign actual values to train

import sys

def saveTensor(a):
    # Using pickle to save to file (Source: https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file)
    output = open('C:\\Users\\Davis-PC\\lpthw\\data.pkl', 'wb')
    pickle.dump(a, output)
    output.close()

    #Can use pickle to load the 3D matrix back into the program (Same source as above)
    pkl_file = open('C:\\Users\\Davis-PC\\lpthw\\data.pkl', 'rb')
    a = pickle.load(pkl_file)
    #pprint.pprint(a)
    pkl_file.close()
    print('Success')
    return a

# 10/27/2018 - right now, this function is not needed. However, I may use it eventually to load data (same as statement in certainCooccurrence now)
def loadTensor():
    #Can use pickle to load the 3D matrix back into the program (Same source as above)
    pkl_file = open('C:\\Users\\Davis-PC\\lpthw\\data.pkl', 'rb')
    a = pickle.load(pkl_file)
    #pprint.pprint(a)
    pkl_file.close()
    supervisedAddition(a)
    return a;

#Definition to view tensor (all, one row, etc)
def printTensor(a, authTokens, title, numTexts):
    f = open("C:\\Users\\Davis-PC\\lpthw\\after" + title + "TensorIndex.out", 'w')
    default_stdout = sys.stdout
    sys.stdout = f
    print("ID1,Name1,ID2,Name2,Score")
    for obj in authTokens:
        for obj2 in authTokens:
            for num in range(numTexts+1):
                if a[int(obj.ID), int(obj2.ID), num] > 0:
                    print("Text:", num, "-", obj.ID,',', obj.name, ',', obj2.ID, ',', obj2.name, ',', a[int(obj.ID), int(obj2.ID), num],sep='')
    f.close()
    sys.stdout = default_stdout

# We need to normalize our current text array based on the the highest used entity (THE HUB)
def normalizeTensor(a, maxID, numTexts):
    print("Starting normalizing tensor")
    maxScore = 0
    maxIDInt = max(maxID)
    for i in range(maxIDInt): #only need to look at a[i,i,numText] because looking for the hub (highest score)
             if maxScore < a[int(i), int(i), int(numTexts)]:
                maxScore = a[int(i), int(i), int(numTexts)]
    print("Max score is:", maxScore)
    for i in range(maxIDInt):
        for j in range(maxIDInt):
            if a[int(i), int(j), int(numTexts)] > .01:
                a[int(i), int(j), int(numTexts)] /= maxScore
            elif a[int(i), int(j), int(numTexts)] > 0 and a[int(i), int(j), int(numTexts)] > .01 :
                a[int(i), int(j), int(numTexts)] =.01
#        per = int((i/maxIDInt)*100)
#        if per % 10 == 0:
#            print("STEP 5 of 6: normalizeTensor is:" + str(per) + '% Complete')
    return a

#In order to get better performance, create an index of normalized values of all text scores in the tensor
def calculateIndex(a, maxID, numTexts):
    print("Starting index calculation")
    maxScore = 0
    maxIDInt = max(maxID)
    #this will create an index at location a[i,j,0] that will hold the sum of all
    #Reset a[i,j,0]
    for i in range(maxIDInt+1):
        for j in range(maxIDInt+1):
            a[i,j,0] = 0

    for k in range(1, numTexts+1):
        for i in range(maxIDInt+1):
            for j in range(maxIDInt+1):
                a[i,j,0] += a[i,j,k]
    for i in range(maxIDInt+1):
        for j in range(maxIDInt+1):
             if maxScore < a[int(i), int(j), int(0)]:
                maxScore = a[int(i), int(j), int(0)]
    print("The maxScore is:", maxScore)
    # This will create an AVERAGE for all values based on the given number of texts
    for i in range(maxIDInt+1):
        for j in range(maxIDInt+1):
#######            a[i,j,0] /= numTexts
            a[i,j,0] /= maxScore
