def tensorConnections(a, numTexts, maxID, totalConnections):
    for i in range(max(maxID)):
        for num in range(int(numTexts)+1):
            if a[int(i), int(i), int(num)]>0:
                totalConnections += a[int(i), int(i), int(num)]
            #Ability to pull in the "text" index
            if a[int(i), int(0), int(num)]>0:
                totalConnections += a[int(i), int(0), int(numTexts)]
                #print("a[", i,",", str(0),",", numTexts," is:", a[int(i), int(0), int(numTexts)])
                #print("Total Connections now equal:", totalConnections)

        #for num2 in range(int(numTexts)+1):
        #    if a[int(i), int(i), int(num2)]>0:
        #       totalConnectionsAll += 1
    return totalConnections#, totalConnectionsAll

#What is the probability that the candidate A will happen on its own P(A)
def calculateP_A(a, authTokens, P_A_Tracker, numTexts, objA, maxID, totalConnections):
    for cand in objA.ambCandidates:
        for count in range(max(maxID)):
            # use numTexts+1 to iterate through all tensor texts (including current)
            for num in range(int(numTexts)+1):
                if int(cand) != int(count):
                    P_A_Tracker[int(cand)] += a[int(cand),int(count), int(num)]
        #print("objA.ID", objA.ID, "int(cand) = ", cand, "P_A_Tracker[int(cand)] = ", P_A_Tracker[cand], "totalConnections = ", totalConnections)
        #Add the supervised text connection
        P_A_Tracker[int(cand)] += a[int(cand), int(0), int(numTexts)]
        if a[int(cand), int(0), int(numTexts)] > 0:
            print("a[", cand ,",0,",numTexts,"] equals", a[int(cand), int(0), int(numTexts)])
        P_A_Tracker[int(cand)] /= totalConnections

        #print("PA of token", objA.ID, "and candidate ID of", cand, "has a PA of:", P_A_Tracker[int(cand)])
    return P_A_Tracker

#What is the probability that all of the connections in the coccurence window will happen given A is there P(B|A)
def calculateP_B_A(vardistance, a, P_B_A_Tracker, textTokens, numTexts, objA, maxID, totalConnections):
    for cand in objA.ambCandidates:
        candidateTracker = [0] * (max(maxID)+1)
        for obj2 in textTokens:
            if candidateTracker[obj2.assignedAuthID] != 1 and obj2.assigned is True and abs(obj2.ID - objA.ID) <= vardistance:# and int(obj2.assignedAuthID) != int(cand)): #and obj2.ambiguous == False
#                if objA.ID == 6548:
#                    print("B",cand, obj2.assignedAuthID)
                for num in range(int(numTexts)+1):
                    P_B_A_Tracker[int(cand)] += a[int(obj2.assignedAuthID), int(cand), int(num)]/totalConnections

#                    if objA.ID == 300:
#                        print("Updating P_B_A_Tracker for", cand, "matching", obj2.assignedAuthID, "with a score of",a[int(obj2.assignedAuthID), int(cand), int(num)] )
                candidateTracker[obj2.assignedAuthID] = 1
                # Add the text connection to it
                P_B_A_Tracker[int(cand)] += a[int(obj2.assignedAuthID), int(0), int(numTexts)]/totalConnections
    return P_B_A_Tracker

# What is the probability that all of the connections will happen on their own P(B)
def calculateP_B(vardistance, a, P_B_Tracker, textTokens, numTexts, objA, maxID, totalConnections):
    candidateTracker = [0] * (max(maxID)+1)
    prodDenominator = 0
    for obj2 in textTokens:
        if(candidateTracker[obj2.assignedAuthID] != 1 and obj2.assigned is True and abs(obj2.ID - objA.ID) <= vardistance): #and obj2.ambiguous == False
            candidateTracker[obj2.assignedAuthID] = 1
            prodDenominator += totalConnections
            for num in range(int(numTexts)+1):
                P_B_Tracker[int(objA.ID)] += a[int(obj2.assignedAuthID),int(obj2.assignedAuthID),int(num)]
            P_B_Tracker[int(objA.ID)] += a[int(obj2.assignedAuthID), int(0), int(numTexts)]
    #print("P_B_Tracker for", objA.ID, " value is:", P_B_Tracker[int(objA.ID)], "Total Connections now", totalConnections)
    if prodDenominator > 0:
        P_B_Tracker[int(objA.ID)] /= prodDenominator
    return P_B_Tracker
