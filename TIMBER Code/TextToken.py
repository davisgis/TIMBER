class TextTokens(object):
    def __init__(self, ID, tokenText, assigned, assignedAuthID, pos, ambiguous, tokenGreek, tokenGreekSurname, assignType, type, score, ambCandidates = [], ambCandScore = []):
        self.ID = ID
        self.tokenText = tokenText
        self.assigned = assigned
        self.assignedAuthID = assignedAuthID
        self.pos = pos
        self.ambiguous = ambiguous
        self.tokenGreek = tokenGreek
        self.tokenGreekSurname = tokenGreekSurname
        self.assignType = assignType
        self.type = type
        self.score = score
        self.ambCandidates = ambCandidates
        self.ambCandScore = ambCandScore
        #Add the calculated score here to print on each tag


textTokens = []
