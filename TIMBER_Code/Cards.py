import numpy as np

def printTokenCards(textobj):
    for obj in textobj:
        #if (len(obj.ambCandidates) == 1):
        if (len(obj.ambCandidates) > 0 and obj.assigned is False):
            print(obj.ID, obj.tokenText, obj.assigned, obj.assignedAuthID, obj.pos, obj.ambiguous, obj.tokenGreek, obj.ambCandidates)

