import csv
import numpy as np
import pickle
import hickle as hkl

def loadBulk(authorityFile, baseMaxIndex, MaxID, numTexts):
    #numTexts = 2 #This includes the index of 0
    #right now, let's set it to allow 100 texts
    bulkArray = np.zeros((3150, 3150, baseMaxIndex+1),dtype=np.float16)
    with open(authorityFile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        entitySeed = 1/int(max(MaxID))
        #textSeed = 1/(int(numTexts)+1)
        print("Seeding the tensor with supervised value", str(entitySeed))
        print("This may take some time on the first text")
        for entity in reader:
            for i in range(1,36):
                connectionStr = "C" + str(i)
                connection = int(entity[connectionStr])
                if int(connection) > 0:
                    bulkArray[int(entity["ID"]), int(connection), int(0)] = 1
                    bulkArray[int(connection), int(entity["ID"]), int(0)] = 1
                    bulkArray[int(entity["ID"]), int(entity["ID"]), int(0)] = 1
                    bulkArray[int(connection), int(connection), int(0)] = 1
                    #bulkArray[int(entity["ID"]), int(connection), int(baseMaxIndex)] = 1
                    #bulkArray[int(connection), int(entity["ID"]), int(baseMaxIndex)] = 1
                    #print("Now connecting: ", entity["ID"], "-", connection)
            #Adding entities found in texts
            for j in range(1,6):
                connectionStr = "T" + str(j)
                connection = int(entity[connectionStr])
                if int(connection) > 0:
                    bulkArray[int(entity["ID"]), int(0), int(j)] = connection #textSeed
                    #bulkArray[int(entity["ID"]), int(connection), int(baseMaxIndex)] = 1
                    #bulkArray[int(connection), int(entity["ID"]), int(baseMaxIndex)] = 1
                    print("Now connecting: ", entity["ID"], "-", int(0), "-", int(j),":", connection)
        hkl.dump(bulkArray, 'C:\\Texts\\DataFiles\\data.hkl', mode='w')
    return bulkArray
