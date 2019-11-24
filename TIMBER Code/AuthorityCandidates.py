import nltk
from nltk import word_tokenize
from nltk.tag import pos_tag
from urllib import request
from nltk.corpus import stopwords
import csv




def findAuthorityCandidates(authorityFile, TextList2, title):
    stop_words = set(stopwords.words('english'))
    tagged_pos = pos_tag(TextList2)

    name = []

    with open(authorityFile, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # For each entity in the authority file, see if it matches the current text file entity
        for entity in reader:
            if not entity['Name']:
                name.append(entity['Name'])
                #name.append(entity['Name'].capitalize())
            if not entity['Alias1']:
                name.append(entity['Alias1'])
                #name.append(entity['Alias1'].capitalize())
            if not entity['Alias2']:
                name.append(entity['Alias2'])
                #name.append(entity['Alias2'].capitalize())
            if not entity['Alias3']:
                name.append(entity['Alias3'])
                #name.append(entity['Alias3'].capitalize())
            if not entity['Alias4']:
                name.append(entity['Alias4'])
                #name.append(entity['Alias4'].capitalize())
            if not entity['Surname']:
                name.append(entity['Surname'])
                #name.append(entity['Surname'].capitalize())

    propernouns = [word for word,pos in tagged_pos if pos == 'NNP']
    new_words = [propernoun for propernoun in propernouns if propernoun not in name]
    finalwords = [w for w in new_words if w not in stop_words]
    #for word in propernouns:

    #    if word in name:
            #print(word)
    #        propernouns.remove(word)
    with open("C:\\Users\\Davis-PC\\lpthw\\Results_Final\\Candidates\\"+ title + "_Possible_Candidates.csv", "a", encoding='utf8') as f:
        for candidate in finalwords:
            print(candidate, file=f)

    #return propernouns
