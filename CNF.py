from enum import Enum

class operators(Enum):
    AND = 0
    OR = 1
    NOT = 2
    IMPLIES = 3
    EQUALS = 4

class Clause:
    contents = None
    def __init__(self, contents):
        self.contents = contents

    def toLiteral(self):
        #Strip all not's out of the contents, keep them in a seperate list
        nots = list(filter(lambda x: x==operators.NOT,self.contents))
        newContents = list(filter(lambda x: x not in nots, self.contents))
        #If there is more than one String left, it's not a literal
        if (len(newContents)==1) and (isinstance(newContents[0],str)):
            #It's a literal
            symbol = newContents[0]
            sign = len(nots) % 2 == 0
            return Literal(symbol, sign)
        else:
            return self
    def toCNF(self):
        isCNF = map(lambda x: isinstance(x, CNFClause) or x==operators.OR, self.contents)
        if all(isCNF):
            return CNFClause(contents=self.contents)
        else:
            return self

class CNFClause(Clause):
    #A marked, valid clause in CNF
    pass


class Literal(CNFClause):
    symbol = None
    sign = None
    def __init__(self, symbol, sign=True):
        self.symbol = symbol
        self.sign =sign

    def negate(self):
        return Literal(self.symbol, not self.sign)

def impliesReduction(implactingClause):


reductionLaws = {

}

def toCNF(phrase):
    #Phrase is a list of clauses seperated by AND statements
    if len(phrase) == 1:
        working = phrase[0]
        #Try to convert working to a literal
        working = working.toLiteral()
        if isinstance(working,Literal):
            return working
        #Otherwise we have to break down the operators
    else:
        #Reduce all sub-clauses to CNF
        print(list(map(lambda x: toCNF([x]), phrase)))



simpleLiteralClause = [Clause(['a']), Clause(['b'])]
print(toCNF(simpleLiteralClause))

