import numpy as np
import io
import csv
import nltk
from nltk import word_tokenize
from tkinter import *
from SupervisedAddition import *
from urllib import request
from updateTensor import update
from TextToken import TextTokens, textTokens
from AuthTokens import AuthTokens, authTokens
from PyPDF2 import PdfFileReader, PdfFileWriter
from TensorCreation import loadTensor, printTensor, normalizeTensor, calculateIndex
from Cards import printTokenCards
import pprint, pickle
import time, datetime
from TensorBulkLoad import loadBulk
import hickle as hkl
import sys
from AuthorityCandidates import findAuthorityCandidates
import cltk
from cltk.stem.lemma import LemmaReplacer
from BayesScore import *
import math
from nltk.tag import pos_tag


#--------------------------------------------------------------------------------------------------
#            Step 1: Connect to the Authority File to find the Maximum number of entities
#--------------------------------------------------------------------------------------------------
def connection():
    #FOR PDFS!!!!!
    #output = PdfFileWriter()
    #input1 = PdfFileReader(open("c://sayings-of-the-desert-fathers.pdf", "rb"))
    #page = input1.getPage(14)
    #print("title = %s" % page.extractText())
    # FIND THE MAX VALUE ID IN THE ENTITY AUTHORITY FILE. This is needed for the matrix size
    MaxID = []
    #with open('C:\\Texts\\AuthorityFile\\NT_People_Places.csv', encoding='utf-8') as csvfile:
    #with open('C:\\Texts\\AuthorityFile\\AllwGreek.csv', encoding='utf-8') as csvfile:
    with open(authorityFile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            MaxID.append((int(row['ID'])))
    print('MaxID equals: ', max(MaxID))
    #print('Cooccurrence Variable = ', vardistance)
    #print("connection() complete")
    csvfile.close()
    return MaxID

#---------------------------------------------------------------------------------------------------------
#       STEP TWO: Read in the raw text file either from URL or on system
#               - Note: this can be .txt or .pdf (look at code above)
#---------------------------------------------------------------------------------------------------------
def readText():#filepath):
    if language == 'English':
        # Using NLTK Toolkit for NLP and Gutenberg project for KJV text files.
        if urlSelection is True:
            url = urlText
            response = request.urlopen(url)
            raw = response.read().decode('utf8')
        else:
            raw = rawText.read()
        #raw = "God chose Zebedee to be the father of John"
        type(raw).encode('utf-8')
        tokens = word_tokenize(raw)
        pos_tokens = pos_tag(tokens)
        propernouns = [pos for word,pos in pos_tokens]# if pos == 'NNP']
        TextList = nltk.Text(tokens)
        return TextList, propernouns
        #########GREEK http://docs.cltk.org/en/latest/greek.html#lemmatization
    elif language == 'Greek':
        #url = 'http://www.gutenberg.org/files/31802/31802-0.txt' #Greek New Testament
        if urlSelection is True:
            url = urlText
            response = request.urlopen(url)
            raw = response.read().decode('utf8')
        else:
            raw = rawText.read()
        #f = open('C:\\Texts\\MatthewGreek.txt')
        #raw = f.read().decode('utf8')
        #raw = 'τὰ γὰρ πρὸ αὐτῶν καὶ τὰ ἔτι παλαίτερα σαφῶς μὲν εὑρεῖν διὰ χρόνου πλῆθος ἀδύνατα ἦν'
        type(raw).encode('utf-8')
        tokens = word_tokenize(raw)
        lemmatizer = LemmaReplacer('greek')
        #print(lemmatizer.lemmatize(tokens))
        TextList = lemmatizer.lemmatize(tokens)
        propernouns = [0] * len(TextList)
        return TextList, propernouns


#---------------------------------------------------------------------------------------------------
#       STEP THREE: Open Authority File and Search the text for entity matches
#---------------------------------------------------------------------------------------------------
def entityMatch():
    TextList2, propernouns = readText()
    textTokens.clear()
    authTokens.clear()
    # Loop through the list depending on the size of the text (ie: how many tokens)
    # First, print out the max number of tokens in the text to the screen
    print('Total Tokens:', len(TextList2))
    #with open('C:\\Texts\\AuthorityFile\\NT_People_Places.csv', encoding='utf-8') as csvfile:
    #with open('C:\\Texts\\AuthorityFile\\AllwGreek.csv', encoding='utf-8') as csvfile:
    with open(authorityFile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # For each entity in the authority file, see if it matches the current text file entity
        for entity in reader:
            authTokens.append(AuthTokens(int(entity['ID']), entity['Name'], entity['Type'], entity['Surname'], entity['Alias1'], entity['Alias2'], entity['Alias3'],entity['Alias4'], entity['Alias5'],0, entity['Greek'], entity['GreekSurname'], entity['GreekAlias'], entity['GreekAlias2'], False))
    for i in range(len(TextList2)):
        #Creating a token object for every word in the text
        candidateList = []
        for card in authTokens:
            if language == "English":
                #Added this logic in order to find a surname before certainAbiguity()
                #if i > 0 and i < len(TextList2)-1:
                    if TextList2[i].isupper():
                        if TextList2[i] == card.name.capitalize() or TextList2[i] == card.surname.capitalize() or TextList2[i]  == card.alias1.capitalize()  or TextList2[i] == card.alias2.capitalize()  or TextList2[i]  == card.alias3.capitalize()  or TextList2[i]  == card.alias4.capitalize() or TextList2[i]  == card.alias5.capitalize():
                            candidateList.append(int(card.ID))
                #    else:
                #        if TextList2[i] == card.name or (TextList2[i] == card.name and TextList2[i-1] == card.surname) or (TextList2[i] == card.name and TextList2[i+1] == card.surname) or TextList2[i]  == card.alias1  or TextList2[i]  == card.alias2  or TextList2[i]  == card.alias3  or TextList2[i]  == card.alias4:
                #            testList.append(int(card.ID))
                #else:
                #    if TextList2[i].isupper():
                #        if TextList2[i].capitalize() == card.name.capitalize() or TextList2[i].capitalize()  == card.alias1.capitalize()  or TextList2[i].capitalize() == card.alias2.capitalize()  or TextList2[i].capitalize()  == card.alias3.capitalize()  or TextList2[i].capitalize()  == card.alias4.capitalize():
                #            testList.append(int(card.ID))
                    else:
                        if TextList2[i] == card.name or TextList2[i] == card.surname or TextList2[i] == card.alias1  or TextList2[i]  == card.alias2  or TextList2[i]  == card.alias3  or TextList2[i]  == card.alias4 or TextList2[i]  == card.alias5:
                                candidateList.append(int(card.ID))

        #NOTE: Simon Peter is a unique case of a name change
        #       is an alias, a surname, and connected to self
        #   So, in KB I had to make Name, Surname, Alias1, and connection on 6396
                    #if i == 2513:
                    #    print("Found candidate for text token 2513: ", card.ID)
            if language == "Greek":
                if card.greekLemma == TextList2[i] or card.greekSurname == TextList2[i] or card.greekAlias == TextList2[i] or card.greekAlias2 == TextList2[i]:
                    candidateList.append(int(card.ID))

        if TextList2[i] == '<':
            print("FOUND A <")
        if TextList2[i] != '<':
            ambCandScoreList = []
            textTokens.append(TextTokens(i, TextList2[i], False, False, propernouns[i], False, card.greekLemma, card.greekSurname, "Unassigned", "Unknown", 0, candidateList, ambCandScoreList))
    csvfile.close()
    return TextList2

#------------------------------------------------
#   Programatically find the window Distance
#------------------------------------------------
def calculateCooccurenceDistance(TextList2):
    counter = 0
    distance = 0
    sentenceCount = 0

    for i in TextList2:
        #print(i, distance, sentenceCount)
        counter += 1
        if i == "." or i == "?" or i == "!":
            distance += counter
            sentenceCount += 1
            counter = 0
    avgSentenceLength = distance / sentenceCount
    #avgSentenceLength /= 2
    matchWindowDistance = math.floor(avgSentenceLength/2)
    print("The average sentence length / 2 is: ", str(matchWindowDistance))
    return matchWindowDistance

#-------------------------------------------------------------------------------------------
#       STEP FOUR: Determine if textTokens are ambiguous
#-------------------------------------------------------------------------------------------
def determineAmbiguity():
    # Loop through, but needs to be -1 because the matrix starts at 0
    #print("Starting ambiguous check...")
    for obj in textTokens:
        if (len(obj.ambCandidates) > 1):
            obj.ambiguous = True


#----------------------------------------------------------------------------------------------------------------
# STEP FIVE: Use the text token objects to calculate the certain cooccurence
#        Note: This only uses text token objects
#----------------------------------------------------------------------------------------------------------------
def calculateCertainCooccurrence(numTexts, maxID):
    # Create a matrix that is the size of the authority file (the CSV file)
    #a = np.zeros((max(MaxID) + 1, max(MaxID) + 1, 1))
    #a = loadTensor()
    #print("Tensor is created...")
    #[Algorithm confirmed on 6/3]
    for obj in textTokens:
        if(len(obj.ambCandidates) == 1 and obj.assigned == False):
            #If amCandidates == 1, then it is a certainty that it needs to be tagged regardless of connections
            obj.assigned = True
            obj.assignedAuthID = obj.ambCandidates[0]
            obj.assignType = "Certain"
            obj.score = 1
            a[int(obj.ambCandidates[0]), int(obj.ambCandidates[0]), int(numTexts)] += 1
            #if obj.ID == 10527:
            #    print("########### Found 10527 with obj.assigned == ", obj.assigned, obj.ambiguous)
            candidateTracker = [0] * (max(maxID)+1)
            for obj2 in textTokens:
                if (len(obj2.ambCandidates) == 1):
                    if  run > 0 and len(obj.ambCandidates) == 1 and abs(obj2.ID - obj.ID) < matchWindowDistance and  obj.assignedAuthID != obj2.ambCandidates[0] and obj.ID != obj2.ID and obj.ambiguous is False and obj2.ambiguous is False and candidateTracker[obj2.assignedAuthID] !=1:# and obj.assigned is False:
                        a[int(obj.ambCandidates[0]), int(obj2.ambCandidates[0]), int(numTexts)] += 1 #(1 / (abs(obj2.ID - obj.ID))) #This loads to text specific array
                        #if obj.ID == 9394:
                            #print("############## THE SCORE for ",obj.ambCandidates[0], " x ", obj2.ambCandidates[0], " IS: ", a[int(obj.ambCandidates[0]), int(obj2.ambCandidates[0]), int(numTexts)])
                        a[int(obj2.ambCandidates[0]), int(obj.ambCandidates[0]), int(numTexts)] += 1 #(1 / (abs(obj2.ID - obj.ID))) #This loads to text specific array
                        obj.assigned = True
                        obj.score = 1
                        obj.assignedAuthID = obj.ambCandidates[0]
                        candidateTracker[obj.assignedAuthID] = 1
                        obj.assignType = "Certain"
                        obj2.assigned = True
                        obj2.assignedAuthID = obj2.ambCandidates[0]
                        obj2.score = 1
                        obj2.assignType = "Certain"
                    ####NOTE: 6/14/2019- in order to keep the max score down, let's try without this logic (ie: God x God and Jesus x Jesus not max)
                    #elif (obj.ID == obj2.ID):
                        #a[int(obj.ambCandidates[0]), int(obj.ambCandidates[0]), int(0)] += 1
                    #    a[int(obj.ambCandidates[0]), int(obj.ambCandidates[0]), int(numTexts)] += .1
                    #    obj.assigned = True
                    #    obj.assignedAuthID = obj.ambCandidates[0]
                    #    obj.assignType = "Self"
    #print("Text token: ", obj.ID, obj.tokenText, "has a certain match with a score of:", a[int(obj.ambCandidates[0]), int(obj2.ambCandidates[0]), int(0)])

    # Using pickle to save to file (Source: https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file)
####    output = open('C:\\Texts\\data.pkl', 'wb')
####    pickle.dump(a, output)
####    output.close()

    #Can use pickle to load the 3D matrix back into the program (Same source as above)
####    pkl_file = open('C:\\Texts\\data.pkl', 'rb')
####    a = pickle.load(pkl_file)
####    #pprint.pprint(a)
####    pkl_file.close()
    #print("calculateCertainCooccurence() complete")
    return a

def calculateSurname(a, matchWindowDistance, numTexts, run):
        #First, see if you add the "alias" to the original if it will find a match (Mary Magdalene, Simon Peter, Judas Iscariot, and ...Arimathaea, named Joseph (when they are in front)
        #[Algorithm confirmed on 6/3; added logic on 6/10]
        for textobj in textTokens:
            if (len(textobj.ambCandidates) > 0 and textobj.assigned is False):
                for authobj in authTokens:
                    if language == 'English':
                        if textobj.tokenText == authobj.name:
                            for i in range(len(textobj.ambCandidates)):
                                for j in range (1, 3): #look for the surname within 3 tokens. Was 6, but "other Mary," got me
                                    #Surname logic for English. Note: exact same as Greek except for name of the surname field in object
                                    if j > 0 and textobj.ID > 10 and authobj.ID == textobj.ambCandidates[i] and len(authobj.surname) > 0 and ((textobj.tokenText + " " + textTokens[textobj.ID + j].tokenText == authobj.name + " " + authobj.surname and textobj.tokenText != textTokens[textobj.ID + j].tokenText) or (textobj.tokenText + " " + textTokens[textobj.ID - j].tokenText == authobj.name + " " + authobj.surname and textobj.tokenText != textTokens[textobj.ID - j].tokenText)):
                                        #print(textobj.ID, "-",textobj.tokenText, "-",textTokens[textobj.ID + j].tokenText, "-",textTokens[textobj.ID - j].tokenText)
                                        textobj.assignedAuthID = textobj.ambCandidates[i]
                                        textobj.assigned = True
                                        textobj.assignType = "Surname"
                                        if (textobj.tokenText + " " + textTokens[textobj.ID + j].tokenText == authobj.name + " " + authobj.surname):
                                            textTokens[textobj.ID + j].assignedAuthID = textobj.ambCandidates[i]
                                            textTokens[textobj.ID + j].assigned = True
                                            textTokens[textobj.ID + j].assignType = "Surname"
                                        elif (textobj.tokenText + " " + textTokens[textobj.ID - j].tokenText == authobj.name + " " + authobj.surname):
                                            textTokens[textobj.ID - j].assignedAuthID = textobj.ambCandidates[i]
                                            textTokens[textobj.ID - j].assigned = True
                                            textTokens[textobj.ID - j].assignType = "Surname"
                                        # If the both name and surname are ambiguous, then it will double count the person/place
                                        # For example, Mary Magdalene was getting a super high score, so no count on Surname
                                        # However, both Simon and Peter are ambiguous, so it needs to be counted.
                                        #if textobj.ambiguous is True and (textTokens[textobj.ID + j].ambiguous is True or textTokens[textobj.ID - j].ambiguous is True):
                                        #    a[int(authobj.ID), int(authobj.ID), int(numTexts)] += 1 #1

                                #Surname logic for English. Note: exact same as English except for name of the surname field in object
                    elif language == 'Greek':
                        if textobj.tokenText == authobj.greekLemma:
                            for i in range(len(textobj.ambCandidates)):
                                for j in range (1, 3): #look for the surname within 6 tokens
                                    #if textobj.assigned == False and j > 0 and textobj.ID > 10 and authobj.ID == textobj.ambCandidates[i] and len(authobj.greekSurname) > 0 and ((textobj.tokenText + " " + textTokens[textobj.ID + j].tokenText == authobj.greekLemma + " " + authobj.greekSurname and textobj.tokenText != textTokens[textobj.ID + j].tokenText )): #or (textobj.tokenText + " " + textTokens[textobj.ID - j].tokenText == authobj.greekLemma + " " + authobj.greekSurname and textobj.tokenText
                                    if j > 0 and textobj.ID > 10 and authobj.ID == textobj.ambCandidates[i] and len(authobj.greekSurname) > 0 and ((textobj.tokenText + " " + textTokens[textobj.ID + j].tokenText == authobj.greekLemma + " " + authobj.greekSurname and textobj.tokenText != textTokens[textobj.ID + j].tokenText) or (textobj.tokenText + " " + textTokens[textobj.ID - j].tokenText == authobj.greekLemma + " " + authobj.greekSurname and textobj.tokenText != textTokens[textobj.ID -j].tokenText)):

                                        #print(textobj.ID, "-",textobj.tokenText, "-",textTokens[textobj.ID + j].tokenText, "-",textTokens[textobj.ID - j].tokenText)
                                        textobj.assignedAuthID = textobj.ambCandidates[i]
                                        textobj.assigned = True
                                        textobj.assignType = "Surname"
                                        if textobj.tokenText + " " + textTokens[textobj.ID + j].tokenText == authobj.greekLemma + " " + authobj.greekSurname:
                                            textTokens[textobj.ID + j].assignedAuthID = textobj.ambCandidates[i]
                                            textTokens[textobj.ID + j].assigned = True
                                            textTokens[textobj.ID + j].assignType = "Surname"
                                        #a[int(authobj.ID), int(authobj.ID), int(0)] += .5 #1
                                        a[int(authobj.ID), int(authobj.ID), int(numTexts)] += 1 #1


def surnameScoring(a, matchWindowDistance, numTexts, run, maxID):
    for textobj in textTokens:
 #------------------------------------------------------------------------
            # Making connections with Surname matches and tokens within match window
            #    Score is calculated using a Bayesian approach
            #------------------------------------------------------------------------
        if textobj.assigned == True and run > 0 and (textobj.assignType == "Surname") and (textobj.ID > 2 and (textobj.assignedAuthID != textTokens[textobj.ID -1].assignedAuthID or textobj.assignedAuthID != textTokens[textobj.ID -2].assignedAuthID )):
            #print("Looking for connections to:", textobj.ID)
            #print("textTokens[textobj.ID -1] is ", textTokens[textobj.ID -1].assignedAuthID)
            #print("textTokens[textobj.ID -2] is ", textTokens[textobj.ID -2].assignedAuthID)
            totalConnections = 0
            totalConnections = tensorConnections(a, numTexts, MaxID,totalConnections)
            candidateTracker = [0] * (max(maxID)+1)
            for i in range(matchWindowDistance*-1, matchWindowDistance+1):
                if textobj.ID + i > 0 and textobj.ID + i < len(textTokens)-1:
                    # Use a Bayesian Scoring model for surname, as well
                    P_A_Total = 0
                    P_A = 0
                    P_B_A_Total = 0
                    P_B_A = 0
                    P_B = 0
                    P_B_Total = 0
                    P_A_B = 0
                    P_A_B = 0
                    if candidateTracker[textTokens[textobj.ID + i].assignedAuthID] != 1 and textTokens[textobj.ID + i].assigned is True and textTokens[textobj.ID + i].assigned > 0 and i != 0:
                        if textobj.assignType == "Surname" and textTokens[textobj.ID + i].assignedAuthID != textobj.assignedAuthID and textTokens[textobj.ID + i].assigned is True:
                            for num in range(int(numTexts)+1):
                                if int(textobj.assignedAuthID) != int(textTokens[textobj.ID + i].assignedAuthID):
                                    P_B_A_Total += a[int(textobj.assignedAuthID),int(textTokens[textobj.ID + i].assignedAuthID), int(num)]
                                for j in range(max(MaxID)+1):
                                    if int(textobj.assignedAuthID) != int(j):
                                        P_A_Total += a[int(textobj.assignedAuthID), int(j), int(num)]
                                    if int(textTokens[textobj.ID + i].assignedAuthID) != int(j):
                                        P_B_Total += a[int(textTokens[textobj.ID + i].assignedAuthID), int(j), int(num)]
                            P_A = P_A_Total/totalConnections
                            P_B_A = P_B_A_Total/totalConnections
                            P_B = P_B_Total/totalConnections
                            if P_B > 0:
                                P_A_B = (P_A * P_B_A)/P_B
                            else:
                                P_A_B = 0
                            #print("PA Total", P_A_Total)
                            #print("PBA Total", P_B_A_Total)
                            #print("PB Total", P_B_Total)
                            #print("Total Connections", totalConnections)
                            #if P_B_A == 0 or P_B == 0:
                            #    print("PA",P_A)
                            #    print("PB",P_B)
                            #    print("P_B_A",P_B_A)
                            #    print(textobj.assignedAuthID, textobj.tokenText , textTokens[textobj.ID + i].assignedAuthID, textTokens[textobj.ID + i].tokenText)
                            if P_A_B > .00001:
                                score = P_A_B
                            else:
                                score = .00001
                            a[int(textobj.assignedAuthID), int(textTokens[textobj.ID + i].assignedAuthID), int(numTexts)] += 1
                            #a[int(textTokens[textobj.ID + i].assignedAuthID), int(textobj.assignedAuthID), int(numTexts)] += 1
                            # Writing dissertation noticed this was already done above and changed from alias to surname
                            a[int(textobj.assignedAuthID), int(textobj.assignedAuthID), int(numTexts)] += 1
                            a[int(textTokens[textobj.ID + i].assignedAuthID), int(textTokens[textobj.ID + i].assignedAuthID), int(numTexts)] += 1
                            #print(textobj.ID, "-", textobj.tokenText, textTokens[textobj.ID + i].ID, "-", textTokens[textobj.ID + i].tokenText, "score is", score)
                            textobj.score = score
                            textTokens[textobj.ID + i].score = score
                            candidateTracker[textTokens[textobj.ID + i].assignedAuthID] = 1


#------------------------------------------------------------------------------------------
# STEP SIX: Calculating the score for each ambiguous candidate
#             Note: this is the heart of the dissertation
#-------------------------------------------------------------------------------------------------
def calculateAmbiguous(a, matchWindowDistance, TextList2, numTexts, MaxID, run, noMatch, totalConnections):
    # Determining the ambiguous candidate with the highest score with cooccurence
    for obj in textTokens:
        if(obj.ambiguous is True and obj.assigned is False):
            vardistance = matchWindowDistance #TEMPORARY RESET OF VARDISTANCE
            ccFound = False
            while True:
                if ccFound is False:
                    ambCandScoreList = []
                    P_A_Tracker = [0] * (max(MaxID)+1)
                    P_B_Tracker = [0] * (len(TextList2)+1)
                    P_B_A_Tracker = [0] * (max(MaxID)+1)
                    candidates = [0] * (max(MaxID)+1)
                    calculateP_A(a, authTokens, P_A_Tracker, numTexts, obj, MaxID, totalConnections)
                    calculateP_B(vardistance, a, P_B_Tracker, textTokens, numTexts, obj, MaxID, totalConnections)
                    calculateP_B_A(vardistance, a, P_B_A_Tracker, textTokens, numTexts, obj, MaxID, totalConnections)
                    maxP_A_B = 0
                    maxPosition = 0
                    if(P_B_Tracker[obj.ID]> 0):
                        for i in obj.ambCandidates:
                            if P_B_Tracker[obj.ID] > 0:
                                P_A_B = (P_A_Tracker[int(i)] * P_B_A_Tracker[int(i)]) / P_B_Tracker[obj.ID]
                                #This will be used to print out candidate scores
                                ambCandScoreList.append(P_A_B)
                            else:
                                print("There was an issue with token: ",obj.ID, " PBTracker is",P_B_Tracker[obj.ID] )
                            if P_A_B > maxP_A_B:
                                maxP_A_B = P_A_B
                                maxPosition = i
                    if maxPosition > 0 and run > 0 and obj.assigned is False:#(maxP_A_B > .005 or run > 1):
                        obj.assignedAuthID = maxPosition
                        obj.assigned = True
                        obj.score = maxP_A_B
                        obj.assignType = "Run:"+ str(run) + "/Window =" + str(vardistance)
                        obj.ambCandScore = ambCandScoreList
                        ccFound == True
                        for obj2 in textTokens:
                            if abs(obj2.ID - obj.ID) <= vardistance and obj2.assigned is True and obj.ID != obj2.ID and int(obj2.assignedAuthID) != int(obj.assignedAuthID):
                                #Update a connection between winner and all tokens within vardistance
                                a[int(obj.assignedAuthID), int(obj2.assignedAuthID), int(numTexts)] += 1
                                #a[int(obj2.assignedAuthID), int(obj.assignedAuthID), int(numTexts)] += 1
                                a[int(obj.assignedAuthID), int(obj.assignedAuthID), int(numTexts)] += 1
                                totalConnections += 1
                                #totalConnections = tensorConnections(a, numTexts, MaxID,totalConnections)
                                #a[int(obj2.assignedAuthID), int(obj2.assignedAuthID), int(numTexts)] += maxP_A_B
                    else:
                        noMatch += 1
                if maxPosition == 0 and vardistance <= (math.sqrt(len(TextList2))*2) and run > 1:
                    vardistance += matchWindowDistance*(run*5)
                else:
                    vardistance = matchWindowDistance
                    #if obj.assigned is False:
                    #    obj.assignedAuthID = 0
                    #    obj.assigned = True
                    #    obj.score = 0
                    #    obj.assignType = "NO ASSIGNMENT: Run:"+ str(run) + "/Window =" + str(vardistance)
                    break
    return noMatch, totalConnections

def assignAuthType():
    for obj in textTokens:
        for authObj in authTokens:
            if obj.assignedAuthID == authObj.ID:
                obj.type = authObj.type

#----------------------------------------------------------------------------------------------------
#      STEP SEVEN: Print out the tagged text in xml format
#----------------------------------------------------------------------------------------------------
def printTaggedText():
    with open("C:\\Texts\\Results\\"+ title + ".xml", "a", encoding='utf8') as f:
        print('<?xml version="1.0" encoding="UTF-8"?>', file=f)
        print('<TEI xmlns="http://www.tei-c.org/ns/1.0">', file=f)
        print(' <teiHeader>', file=f)
        print('     <fileDesc>', file=f)
        print('         <titleStmt>', file=f)
        print('             <title>' + title + ' - ' + language + '</title>', file=f)
        print('         </titleStmt>', file=f)
        print('         <publicationStmt>', file=f)
        print('             <p>Original publication in 1885  in a 10 volume set. Retrieved via computer on {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '</p>', file=f)
        print('             <p>Cooccurrence Distance Used: '+ str(matchWindowDistance) +'</p>', file=f)
        print('         </publicationStmt>', file=f)
        print('         <sourceDesc>', file=f)
        print('             <p>Online source from Calvin College: https://www.ccel.org/fathers.html</p>', file=f)
        print('         </sourceDesc>', file=f)
        print('     </fileDesc>', file=f)
        print(' </teiHeader>', file=f)
        print(' <text>', file=f)
        print('     <body>', file=f)
        print('         <p>', end='', file=f)
        for obj in textTokens:
            if obj.assigned is True or obj.assignedAuthID is 'TIE':
                if obj.ambiguous is False:
                    print('\t\t<w xml:id ="', obj.ID, '" type="', obj.pos,'">',sep='', file=f)
                    print('\t\t\t<name ref="',obj.assignedAuthID, '" role="Amb-', obj.ambiguous,',AssignType-', obj.assignType, '" type="', obj.type, '" key="TP">', obj.tokenText,  '</name> ',sep='', file=f)
                    print('\t\t</w>',sep='', file=f)
                else:
                    print('\t\t<w xml:id ="', obj.ID, '" type="', obj.pos,'">',sep='', file=f)
                    print('\t\t\t<name ref="',obj.assignedAuthID, '" role="Amb-', obj.ambiguous,',AssignType-', obj.assignType, '" type="', obj.type, '" key="TP">', obj.tokenText,  '</name> ',sep='', file=f)
                    if showCertainty == 1:
                        for i in range(len(obj.ambCandidates)):
                            #Surname does not have ambiguous score, so need this check
                            if len(obj.ambCandidates) > len(obj.ambCandScore):
                                print("Candidates less than Scores: Surname")
                            else:
                                print('\t\t\t<certainty xmlid="Cand',str(i),'" locus="value" target="#', obj.ambCandidates[i], '" degree="', obj.ambCandScore[i],'" />', sep='', file=f)
                    print('\t\t</w>',sep='', file=f)
            elif obj.pos == 'NNP' and obj.assigned is False and tagPossibleUnknown == 1:
                print('\t\t<w xml:id ="', obj.ID, '" type="', obj.pos,'">',sep='', file=f)
                print('\t\t\t<name ref="',obj.assignedAuthID, '" role="Amb-', obj.ambiguous,',AssignType-POSSIBLE UNKNOWN ENTITY" type="', obj.type, '" key="FN">', obj.tokenText,  '</name> ',sep='', file=f)
                print('\t\t</w>',sep='', file=f)
            else:
                print('\t\t<w xml:id="', obj.ID, '" type="', obj.pos,'">',obj.tokenText,"</w> ",sep='', file=f)
        print('         </p>', file=f)
        print('     </body>', file=f)
        print(' </text>', file=f)
        print('</TEI>',file=f)
        f.close()
#-------------------------------------------------------------------------------------
##########                          MAIN CODE                    #####################
#       This will determine the order in which the above functions will run
#-------------------------------------------------------------------------------------


#for i in range(3,13):
#######################
#   TEXTS IN TENSOR
######################
#numTexts = 1
for i in range(1,2):
    then = time.time() #Time before the operations start
    print('Started at: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    #numTexts = int(input("Which file would you like me to read?"))
    numTexts = i

    # Create possible Candidate file?
    #createCandFile = True
    #createCandFile = input("Would you like for me to provide you with possible missed candidates?")
    createCandFile = "Y"
    if createCandFile == "Y" or createCandFile == "y":
        createCandFile = True
    else:
        createCandFile = False
    # 0: Index
    # 1: Matthew-English [Loaded]
    # 2: Mark-English [Loaded]
    # 3: Luke-English [Loaded]
    # 4: John-English [Loaded]
    # 5: Ante-Nicene Volume 1 [Loaded]
    #------------------------
    authorityFile = 'C:\\Texts\\AuthorityFile\\AllwGreek.csv'
    #rawText = 'http://www.gutenberg.org/files/31802/31802-0.txt'    #NT-Greek
    #if numTexts == 1:
    #    urlText = 'http://www.gutenberg.org/cache/epub/8040/pg8040.txt' #Matthew-English-1
    #    title = '1-Matthew'
    #    urlSelection = True
    if numTexts == 1:
        urlText = 'http://www.gutenberg.org/cache/epub/8040/pg8040.txt' #Matthew-Gutenberg
        #filename = 'C:\\Texts\\Texts\\61-MtUTF8.txt' #Matthew-Vatican
        #rawText  = open(filename, "r", encoding="utf-8")
        title = '1a-Matthew-Greek'
        urlSelection = True
    elif numTexts == 2:
        urlText = 'http://www.gutenberg.org/cache/epub/8041/pg8041.txt' #Mark-English-2
        title = '2-Mark'
        urlSelection = True
    elif numTexts == 3:
        urlText = 'http://www.gutenberg.org/cache/epub/8042/pg8042.txt' #Luke-English-3
        title = '3-Luke'
        urlSelection = True
    elif numTexts == 4:
        urlText = 'http://www.gutenberg.org/cache/epub/8043/pg8043.txt' #John-English-4
        title = '4-John'
        urlSelection = True
        ####################################################
    elif numTexts == 5:
        filename = 'C:\\Texts\\Vol_1_1_1_Clement_of_Rome_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '5_Vol_1_1_1_Clement_of_Rome_Introduction'
        urlSelection = False
    elif numTexts == 6:
        filename = 'C:\\Texts\\Vol_1_1_Clement_of_Rome.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '6_Vol_1_1_Clement_of_Rome_Texts'
        urlSelection = False
    elif numTexts == 7:
        filename = 'C:\\Texts\\Vol_1_2_1_Mathetes_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '7_Vol_1_2_1_Mathetes_Introduction'
        urlSelection = False
    elif numTexts == 8:
        filename = 'C:\\Texts\\Vol_1_2_Mathetes.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '8_Vol_1_1_Mathetes_Texts'
        urlSelection = False
    elif numTexts == 9:
        filename = 'C:\\Texts\\Vol_1_3_a_1_Polycarp_Epistle_to_the_Philippians_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '9_Vol_1_3_a_1_Polycarp_Epistle_to_the_Philippians_Introduction'
        urlSelection = False
    elif numTexts == 10:
        filename = 'C:\\Texts\\Vol_1_3_a_Polycarp_Epistle_to_the_Philippians.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '10_Vol_1_3_a_Polycarp_Epistle_to_the_Philippians'
        urlSelection = False
    elif numTexts == 11:
        filename = 'C:\\Texts\\Vol_1_3_b_1_Polycarp_Martyrdom_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '11_Vol_1_3_b_1_Polycarp_Martyrdom_Introduction'
        urlSelection = False
    elif numTexts == 12:
        filename = 'C:\\Texts\\Vol_1_3_b_Polycarp_Martyrdom.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '12_Vol_1_3_b_Polycarp_Martyrdom'
        urlSelection = False
    elif numTexts == 13:
        filename = 'C:\\Texts\\Vol_1_4_1_Ignatius_Epistles_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '13_Vol_1_4_1_Ignatius_Epistles_Introduction'
        urlSelection = False
    elif numTexts == 14:
        filename = 'C:\\Texts\\Vol_1_4_a_Ignatius_Epistle_to_the_Ephesians.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '14_Vol_1_4_a_Ignatius_Epistle_to_the_Ephesians'
        urlSelection = False
    elif numTexts == 15:
        filename = 'C:\\Texts\\Vol_1_4_b_Ignatius_Epistle_to_the_Magnesians.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '15_Vol_1_4_b_Ignatius_Epistle_to_the_Magnesians'
        urlSelection = False
    elif numTexts == 16:
        filename = 'C:\\Texts\\Vol_1_4_c_Ignatius_Epistle_to_the_Trallians.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '16_Vol_1_4_c_Ignatius_Epistle_to_the_Trallians'
        urlSelection = False
    elif numTexts == 17:
        filename = 'C:\\Texts\\Vol_1_4_d_Ignatius_Epistle_to_the_Philadelphians.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '17_Vol_1_4_d_Ignatius_Epistle_to_the_Philadelphians'
        urlSelection = False
    elif numTexts == 18:
        filename = 'C:\\Texts\\Vol_1_4_e_Ignatius_Epistle_to_the_Romans.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '18_Vol_1_4_e_Ignatius_Epistle_to_the_Romans'
        urlSelection = False
    elif numTexts == 19:
        filename = 'C:\\Texts\\Vol_1_4_f_Ignatius_Epistle_to_the_Smyrnæans.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '19_Vol_1_4_f_Ignatius_Epistle_to_the_Smyrnæans'
        urlSelection = False
    elif numTexts == 20:
        filename = 'C:\\Texts\\Vol_1_4_g_Ignatius_Epistle_to_the_Polycarp.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '20_Vol_1_4_g_Ignatius_Epistle_to_the_Polycarp'
        urlSelection = False
    elif numTexts == 21:
        filename = 'C:\\Texts\\Vol_1_4_h_1_Ignatius_Syriac_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '21_Vol_1_4_h_1_Ignatius_Syriac_Introduction'
    elif numTexts == 22:
        filename = 'C:\\Texts\\Vol_1_4_h_Ignatius_Syriac.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '22_Vol_1_4_h_Ignatius_Syriac'
        urlSelection = False
    elif numTexts == 23:
        filename = 'C:\\Texts\\Vol_1_4_i_1_Ignatius_Spurious_Epistles_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '23_Vol_1_4_i_1_Ignatius_Spurious_Epistles_Introduction'
    elif numTexts == 24:
        filename = 'C:\\Texts\\Vol_1_4_i_Ignatius_Spurious_Epistles.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '24_Vol_1_4_i_Ignatius_Spurious_Epistles'
        urlSelection = False
    elif numTexts == 25:
        filename = 'C:\\Texts\\Vol_1_4_j_1_Ignatius_Martyrdom_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '25_Vol_1_4_j_1_Ignatius_Martyrdom_Introduction'
        urlSelection = False
    elif numTexts == 26:
        filename = 'C:\\Texts\\Vol_1_4_j_Ignatius_Martyrdom.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '26_Vol_1_4_j_Ignatius_Martyrdom'
        urlSelection = False
    elif numTexts == 27:
        filename = 'C:\\Texts\\Vol_1_5_1_Barnabas_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '27_Vol_1_5_1_Barnabas_Introduction'
        urlSelection = False
    elif numTexts == 28:
        filename = 'C:\\Texts\\Vol_1_5_Barnabas.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '28_Vol_1_5_Barnabas'
        urlSelection = False
    elif numTexts == 29:
        filename = 'C:\\Texts\\Vol_1_6_1_Papias_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '29_Vol_1_6_1_Papias_Introduction'
        urlSelection = False
    elif numTexts == 30:
        filename = 'C:\\Texts\\Vol_1_6_Papias.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '30_Vol_1_6_Papias'
        urlSelection = False
    elif numTexts == 31:
        filename = 'C:\\Texts\\Vol_1_7_1_Justin_Martyr_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '31_Vol_1_7_1_Justin_Martyr_Introduction'
        urlSelection = False
    elif numTexts == 32:
        filename = 'C:\\Texts\\Vol_1_7_a_Justin_Martyr_First_Apology.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '32_Vol_1_7_a_Justin_Martyr_First_Apology'
        urlSelection = False
    elif numTexts == 33:
        filename = 'C:\\Texts\\Vol_1_7_b_Justin_Martyr_Second_Apology.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '33_Vol_1_7_b_Justin_Martyr_Second_Apology'
        urlSelection = False
    elif numTexts == 34:
        filename = 'C:\\Texts\\Vol_1_7_c_Justin_Martyr_Dialouge_with_Trypho.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '34_Vol_1_7_c_Justin_Martyr_Dialouge_with_Trypho'
        urlSelection = False
    elif numTexts == 35:
        filename = 'C:\\Texts\\Vol_1_7_d_Justin_Martyr_Discourse_to_the_Greeks.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '35_Vol_1_7_d_Justin_Martyr_Discourse_to_the_Greeks'
        urlSelection = False
    elif numTexts == 36:
        filename = 'C:\\Texts\\Vol_1_7_e_Justin_Martyr_Hortatory_Address_to_the_Greeks.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '36_Vol_1_7_e_Justin_Martyr_Hortatory_Address_to_the_Greeks'
        urlSelection = False
    elif numTexts == 37:
        filename = 'C:\\Texts\\Vol_1_7_f_Justin_Martyr_On_the_Sole_Government_of_God.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '37_Vol_1_7_f_Justin_Martyr_On_the_Sole_Government_of_God'
        urlSelection = False
    elif numTexts == 38:
        filename = 'C:\\Texts\\Vol_1_7_g_Justin_Martyr_On_the_Resurrection.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '38_Vol_1_7_g_Justin_Martyr_On_the_Resurrection'
        urlSelection = False
    elif numTexts == 39:
        filename = 'C:\\Texts\\Vol_1_7_h_Justin_Martyr_Other_Fragments.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '39_Vol_1_7_h_Justin_Martyr_Other_Fragments'
        urlSelection = False
    elif numTexts == 40:
        filename = 'C:\\Texts\\Vol_1_7_i_Justin_Martyr_Martydom.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '40_Vol_1_7_i_Justin_Martyr_Martydom'
        urlSelection = False
    elif numTexts == 41:
        filename = 'C:\\Texts\\Vol_1_8_a_1_Irenaeus_Against_Heresies_Introduction.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '41_Vol_1_8_a_1_Irenaeus_Against_Heresies_Introduction'
        urlSelection = False
    elif numTexts == 42:
        filename = 'C:\\Texts\\Vol_1_8_a_Irenaeus_Against_Heresies.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '42_Vol_1_8_a_Irenaeus_Against_Heresies'
        urlSelection = False
    elif numTexts == 43:
        filename = 'C:\\Texts\\Vol_1_8_b_Irenaeus_Fragments.txt' #Ante-Nicene-5
        rawText  = open(filename, "r")
        title = '43_Vol_1_8_b_Irenaeus_Fragments'
        urlSelection = False
    ################################################################
    volumes = 2
    if volumes == 2:
        if numTexts == 44:
            filename = 'C:\\Texts\\Vol_2_1_1_Pastor_of_Hermas_Introduction.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '44_Vol_2_1_1_Pastor_of_Hermas_Introduction'
            urlSelection = False
        elif numTexts == 45:
            filename = 'C:\\Texts\\Vol_2_1_Pastor_of_Hermas.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '45_Vol_2_1_Pastor_of_Hermas'
            urlSelection = False
        elif numTexts == 46:
            filename = 'C:\\Texts\\Vol_2_2_1_Tatian_Introduction.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '46_Vol_2_2_1_Tatian_Introduction'
            urlSelection = False
        elif numTexts == 47:
            filename = 'C:\\Texts\\Vol_2_2_Tatian.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '47_Vol_2_2_Tatian'
            urlSelection = False
        elif numTexts == 48:
            filename = 'C:\\Texts\\Vol_2_3_1_Theophilus_of_Antioch_Introduction.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '48_Vol_2_3_1_Theophilus_of_Antioch_Introduction'
            urlSelection = False
        elif numTexts == 49:
            filename = 'C:\\Texts\\Vol_2_3_Theophilus_of_Antioch.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '49_Vol_2_3_Theophilus_of_Antioch'
            urlSelection = False
        elif numTexts == 50:
            filename = 'C:\\Texts\\Vol_2_4_1_Athenagoras_Introduction.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '50_Vol_2_4_1_Athenagoras_Introduction'
            urlSelection = False
        elif numTexts == 51:
            filename = 'C:\\Texts\\Vol_2_4_Athenagoras.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '51_Vol_2_4_Athenagoras'
            urlSelection = False
        elif numTexts == 52:
            filename = 'C:\\Texts\\Vol_2_5_1_Clement_of_Alexandria_Introduction.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '52_Vol_2_5_1_Clement_of_Alexandria_Introduction'
            urlSelection = False
        elif numTexts == 53:
            filename = 'C:\\Texts\\Vol_2_5_Clement_of_Alexandria.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '53_Vol_2_5_Clement_of_Alexandria'
            urlSelection = False
            #################################################
            ################################################
        elif numTexts == 54:
            filename = 'C:\\Texts\\Vol_3_1_Tertullian_Apologetics.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '54_Volume_Three_TertullianApologetic_Texts'
            urlSelection = False
        elif numTexts == 55:
            filename = 'C:\\Texts\\Vol_3_2_Tertullian_Anti_Marcion.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '55_Volume_Three_TertullianAnti-Marcion_Texts'
            urlSelection = False
        elif numTexts == 56:
            filename = 'C:\\Texts\\Vol_3_3_Tertullian_Ethical.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '56_Volume_Three_TertullianEthical_Texts'
            urlSelection = False
        elif numTexts == 57:
            filename = 'C:\\Texts\\Vol_4_1_Tertullian_PartFour.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '57_Vol_4_Tertullian_Part_Four_Texts'
            urlSelection = False
        elif numTexts == 58:
            filename = 'C:\\Texts\\Vol_4_2_Minucius_Felix.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '58_Vol_4_Minucius_Felix_Texts'
            urlSelection = False
        elif numTexts == 59:
            filename = 'C:\\Texts\\Vol_4_3_Commodianus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '59_Vol_4_CommodianusTexts'
            urlSelection = False
        elif numTexts == 60:
            filename = 'C:\\Texts\\Vol_4_4_Origen.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '60_Vol_4_Origen_Texts'
            urlSelection = False
        elif numTexts == 61:
            filename = 'C:\\Texts\\Vol_5_1_Hippolytus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '61_Vol_5_Hippolytus_Texts'
            urlSelection = False
        elif numTexts == 62:
            filename = 'C:\\Texts\\Vol_5_2_Cyprian.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '62_Vol_5_Cyprian_Texts'
            urlSelection = False
        elif numTexts == 63:
            filename = 'C:\\Texts\\Vol_5_3_Caius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '63_Vol_5_Caius_Texts'
            urlSelection = False
        elif numTexts == 64:
            filename = 'C:\\Texts\\Vol_5_4_Novatian.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '64_Vol_5_Novatian_Texts'
            urlSelection = False
        elif numTexts == 65:
            filename = 'C:\\Texts\\Vol_6_1_Gregory_Thaumaturgus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '65_Vol_6_Gregory_Thaumaturgus_Texts'
            urlSelection = False
        elif numTexts == 66:
            filename = 'C:\\Texts\\Vol_6_2_Dionysius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '66_Vol_6_Dionysius_Texts'
            urlSelection = False
        elif numTexts == 67:
            filename = 'C:\\Texts\\Vol_6_3_Julius_Africanus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '67_Vol_6_Julius_Africanus_Texts'
            urlSelection = False
        elif numTexts == 68:
            filename = 'C:\\Texts\\Vol_6_4_Anatolius_and_Minor_Writers.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '68_Vol_6_Anatolius_and_Minor_Writers_Texts'
            urlSelection = False
        elif numTexts == 69:
            filename = 'C:\\Texts\\Vol_6_5_Archelaus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '69_Vol_6_Archelaus_Texts'
            urlSelection = False
        elif numTexts == 70:
            filename = 'C:\\Texts\\Vol_6_6_Alexander_of_Lycopolis.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '70_Vol_6_Alexander_of_Lycopolis_Texts'
            urlSelection = False
        elif numTexts == 71:
            filename = 'C:\\Texts\\Vol_6_7_Peter_of_Alexandria.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '71_Vol_6_Peter_of_Alexandria_Texts'
            urlSelection = False
        elif numTexts == 72:
            filename = 'C:\\Texts\\Vol_6_8_Alexander_of_Alexandria.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '72_Vol_6_Alexander_of_Alexandria_Texts'
            urlSelection = False
        elif numTexts == 73:
            filename = 'C:\\Texts\\Vol_6_9_Methodius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '73_Vol_6_Methodius_Texts'
            urlSelection = False
        elif numTexts == 74:
            filename = 'C:\\Texts\\Vol_6_10_Arnobius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '74_Vol_6_Arnobius_Texts'
            urlSelection = False
        elif numTexts == 75:
            filename = 'C:\\Texts\\Vol_7_1_Lactantius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '75_Vol_7_Lactantius_Texts'
            urlSelection = False
        elif numTexts == 76:
            filename = 'C:\\Texts\\Vol_7_2_Venantius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '76_Vol_7_Venantius_Texts'
            urlSelection = False
        elif numTexts == 77:
            filename = 'C:\\Texts\\Vol_7_3_Asterius_Urbanus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '77_Vol_7_Asterius_Urbanus_Texts'
            urlSelection = False
        elif numTexts == 78:
            filename = 'C:\\Texts\\Vol_7_4_Victorinus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '78_Vol_7_Victorinus_Texts'
            urlSelection = False
        elif numTexts == 79:
            filename = 'C:\\Texts\\Vol_7_5_Dionysius.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '79_Vol_7_Dionysius_Texts'
            urlSelection = False
        elif numTexts == 80:
            filename = 'C:\\Texts\\Vol_7_6_Teaching_of_the_Twelve_Apostles.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '80_Vol_7_Teaching_of_the_Twelve_Apostles_Texts'
            urlSelection = False
        elif numTexts == 81:
            filename = 'C:\\Texts\\Vol_7_7_Constitutions_of_the_Holy_Apostles.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '81_Vol_7_Constitutions_of_the_Holy_Apostles_Texts'
            urlSelection = False
        elif numTexts == 82:
            filename = 'C:\\Texts\\Vol_7_8_Second_Epistle_of_Clement.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '82_Vol_7_Second_Epistle_of_Clement_Texts'
            urlSelection = False
        elif numTexts == 83:
            filename = 'C:\\Texts\\Vol_7_9_Nicene_Creed.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '83_Vol_7_Nicene_Creed_Texts'
            urlSelection = False
        elif numTexts == 84:
            filename = 'C:\\Texts\\Vol_7_10_Early_Liturgies.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '84_Vol_7_Early_Liturgies_Texts'
            urlSelection = False
        elif numTexts == 85:
            filename = 'C:\\Texts\\Vol_8_1_Testaments_of_the_Twelve_Patriarchs.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '85_Vol_8_Testaments_of_the_Twelve_Patriarchs_Texts'
            urlSelection = False
        elif numTexts == 86:
            filename = 'C:\\Texts\\Vol_8_2_Excerpts_of_Theodotus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '86_Vol_8_Excerpts_of_Theodotus_Texts'
            urlSelection = False
        elif numTexts == 87:
            filename = 'C:\\Texts\\Vol_8_3_Two_Epistles_Concerning_Virginity.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '87_Vol_8_Two_Epistles_Concerning_Virginity_Texts'
            urlSelection = False
        elif numTexts == 88:
            filename = 'C:\\Texts\\Vol_8_4_Pseudo-Clementine_Literature.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '88_Vol_8_Pseudo-Clementine_Literature_Texts'
            urlSelection = False
        elif numTexts == 89:
            filename = 'C:\\Texts\\Vol_8_5_Apocrypha_of_the_New_Testament.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '89_Vol_8_Apocrypha_of_the_New_Testament._Texts'
            urlSelection = False
        elif numTexts == 90:
            filename = 'C:\\Texts\\Vol_8_6_Decretals.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '90_Vol_8_Decretals_Texts'
            urlSelection = False
        elif numTexts == 91:
            filename = 'C:\\Texts\\Vol_8_7_Memoirs_of_Edessa_and_Other_Ancient_Syriac_Documents.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '91_Vol_8_Memoirs_of_Edessa_and_Other_Ancient_Syriac_Documents'
            urlSelection = False
        elif numTexts == 92:
            filename = 'C:\\Texts\\Vol_8_8_Remains_of_the_Second_and_Third_Centuries.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '92_Vol_8_Remains_of_the_Second_and_Third_Centuries_Texts'
            urlSelection = False
        elif numTexts == 93:
            filename = 'C:\\Texts\\Vol_9_1_Gospel_of_Peter.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '93_Vol_9_Gospel_of_Peter_Texts'
            urlSelection = False
        elif numTexts == 94:
            filename = 'C:\\Texts\\Vol_9_2_Diatessaron_of_Tatian.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '94_Vol_9_Diatessaron_of_Tatian_Texts'
            urlSelection = False
        elif numTexts == 95:
            filename = 'C:\\Texts\\Vol_9_3_Apocalypse_of_Peter.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '95_Vol_9_Apocalypse_of_Peter_Texts'
            urlSelection = False
        elif numTexts == 96:
            filename = 'C:\\Texts\\Vol_9_4_Vision_of_Paul.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '96_Vol_9_Vision_of_Paul_Texts'
            urlSelection = False
        elif numTexts == 97:
            filename = 'C:\\Texts\\Vol_9_5_Apocalpyse_of_the_Virgin.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '97_Vol_9_Apocalpyse_of_the_Virgin_Texts'
            urlSelection = False
        elif numTexts == 98:
            filename = 'C:\\Texts\\Vol_9_6_Apocalypse_of_Sedrach.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '98_Vol_9_Apocalypse_of_Sedrach_Texts'
            urlSelection = False
        elif numTexts == 99:
            filename = 'C:\\Texts\\Vol_9_7_Testament_of_Abraham.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '99_Vol_9_Testament_of_Abraham_Texts'
            urlSelection = False
        elif numTexts == 100:
            filename = 'C:\\Texts\\Vol_9_8_Acts_of_Xanthippe_and_Polyxena.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '100_Vol_9_Acts_of_Xanthippe_and_Polyxena_Texts'
            urlSelection = False
        elif numTexts == 101:
            filename = 'C:\\Texts\\Vol_9_9_Narrative_of_Zosimus.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '101_Vol_9_Narrative_of_Zosimus_Texts'
            urlSelection = False
        elif numTexts == 102:
            filename = 'C:\\Texts\\Vol_9_10_Epistles_of_Clement.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '102_Vol_9_Epistles_of_Clement_Texts'
            urlSelection = False
        elif numTexts == 103:
            filename = 'C:\\Texts\\Vol_9_11_Apology_of_Aristides_the_Philosopher.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '103_Vol_9_Apology_of_Aristides_the_Philosopher_Texts'
            urlSelection = False
        elif numTexts == 104:
            filename = 'C:\\Texts\\Vol_9_12_Passion_of_the_Scillitan_Martyrs.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '104_Vol_9_Passion_of_the_Scillitan_Martyrs_Texts'
            urlSelection = False
        elif numTexts == 105:
            filename = 'C:\\Texts\\Vol_9_13_Epistle_to_Gregory.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '105_Vol_9_Epistle_to_Gregory_Texts'
            urlSelection = False
        elif numTexts == 106:
            filename = 'C:\\Texts\\Vol_9_14_Origen_Commentary_on_the_Gospel_of_John.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '106_Vol_9_Origen_Commentary_on_the_Gospel_of_John_Texts'
            urlSelection = False
        elif numTexts == 107:
            filename = 'C:\\Texts\\Vol_9_11_Vol_9_15_Origen_Commentary_on_the_Gospel_of_Matthew.txt' #Ante-Nicene-5
            rawText  = open(filename, "r")
            title = '107_Vol_9_Origen_Commentary_on_the_Gospel_of_Matthew_Texts'
            urlSelection = False

    #langInput = input("In what language will the works be? 1 for English, 2 for Greek")
    langInput = "2"
    if langInput == "1":
        language = 'English'
    else:
        language = 'Greek'
    #language = 'Greek'

        #### Enter other information about the text such as time period, etc for TEI
    print("##########################################################################")
    print("The Computer is reading: " + title + " in the " + language + " language")
    print("##########################################################################")
    MaxID = connection()
    now = time.time() #Time after it finished
    print("Connection stopped at: ", now-then, " seconds")

    #Set this flag to 1 if you want to use NLTK to tag all NNP (Proper Nouns) that
    # are not officially tagged
    tagPossibleUnknown = 0
    #Set this flag to 1 if you want to tag other candidates with their score
    showCertainty = 1
    # Do not touch this. It initializes noMatch for further use; not a flag
    noMatch = 0
    if numTexts == 1:
        sizeInput = int(input("How many texts will you be running? We recommend no more than 300"))
        #baseMaxIndex = 25
        baseMaxIndex = sizeInput
        # On the first time, you will run the bulk load
        # IF YOU LEAVE THIS ON THEN IT WILL RECREATE NEW FROM AUTHORITY FILE EACH TIME
        a = loadBulk(authorityFile, baseMaxIndex, MaxID, numTexts)
        now = time.time() #Time after it finished
        print("Bulk load stopped at: ", now-then, " seconds")
            # This initialized run to 1 so that we can print out which ambiguous run we are currently on
    run = 1
    # What value/distance do you want to consider for co-occurrence?
    #vardistance = 20



    # Can use pickle/hickle to load the 3D matrix back into the program (Same source as above)
    #if numTexts > 1:
    #    a = hkl.load('C:\\Texts\\data.hkl')
    #    now = time.time() #Time after it finished
    #    print("Loading tensor into a[] stopped at: ", now-then, " seconds")
    ######    #supervisedAddition(a)
    ######    #print("Starting Total Connections")
    totalConnections = 0
    totalConnections = tensorConnections(a, numTexts, MaxID,totalConnections)
    #print("Total connections equal:", totalConnections)

    print("Beginning entity match. This may take some time on the first run")
    TextList2 = entityMatch()
    now = time.time() #Time after it finished
    print("entityMatch() stopped at: ", now-then, " seconds")

    #This will determine the distance for the match window
    matchWindowDistance = calculateCooccurenceDistance(TextList2)

    determineAmbiguity()
    now = time.time() #Time after it finished
    print("determineAmbiguity stopped at: ", now-then, " seconds")

    calculateSurname(a, matchWindowDistance, numTexts, run)
    now = time.time() #Time after it finished
    print("calculateSurname() stopped at: ", now-then, " seconds")

    a = calculateCertainCooccurrence(numTexts, MaxID)
    now = time.time() #Time after it finished
    print("calculateCertain() stopped at: ", now-then, " seconds")

    surnameScoring(a, matchWindowDistance, numTexts, run, MaxID)
    now = time.time() #Time after it finished
    print("surnameScoring() stopped at: ", now-then, " seconds")

    print("Starting first round of ambiguous calculations")
    noMatch, totalConnections = calculateAmbiguous(a, matchWindowDistance, TextList2, numTexts, MaxID, run, noMatch, totalConnections)
    now = time.time() #Time after it finished
    print("1st round of calculateAmbiguous() stopped at: ", now-then, " seconds")

    # Running the algorithm twice gives the chance for "TIE" to find a new candidate
    print("Starting second round of ambiguous calculations")

    #print("noMatch is:", noMatch, "and run is:", run)
    while True:
        if noMatch > 0 and run < 3:
            run += 1
            #noMatch = 0
            noMatch, totalConnections = calculateAmbiguous(a, matchWindowDistance, TextList2, numTexts, MaxID, run, noMatch, totalConnections)
            now = time.time() #Time after it finished
            print("Round", run, "of calculateAmbiguous() stopped at: ", now-then, " seconds")
        else:
            break
    assignAuthType()

    # Privide a printout of the number of connections in
    totalConnections = 0
    #totalConnectionsAll = 0
    totalConnections = tensorConnections(a, numTexts, MaxID,totalConnections)
    print("Total initial connections equal:", totalConnections)
    #print("Total connections after running", title, " is ", totalConnectionsAll)


    #print the tensor out in format we can see
    if numTexts == 1 or numTexts == 4:
        printTensor(a, authTokens, title, numTexts)
        print("Printing tensor index for: " + title)

    # Create the tensor file for loading next run

    if numTexts == 4:
        hkl.dump(a, 'C:\\Texts\\DataFiles\\data.hkl')
        now = time.time() #Time after it finished
        print("Dumping Tensor into file stopped at: ", now-then, " seconds")

    # This will print the TEI file with persons/places tagged
    printTaggedText()
    print("XML Created")

    if createCandFile == True:
        print("Starting finding possible candidates")
        # Find possible proper nouns that were not matched
        findAuthorityCandidates(authorityFile, TextList2, title)
                            # not in the authority file

    #DO YOUR OPERATIONS HERE

    #rawText.close()

    now = time.time() #Time after it finished
    print("It took: ", now-then, " seconds")
    print('Ended at: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    ###w for w in text4 if w.startsswith(‘ness’)]
    #http://sapir.psych.wisc.edu/programming_for_psychologists/cheat_sheets/Text-Analysis-with-NLTK-Cheatsheet.pdf
