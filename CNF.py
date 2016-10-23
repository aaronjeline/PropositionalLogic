from enum import Enum
class ConversionError(Exception):
    pass

class operators(Enum):
    AND = 0
    OR = 1
    NOT = 2
    IMPLIES = 3
    EQUALS = 4

def conversion(item):
    if isinstance(item, Clause):
        return item.toCNF()
    else:
        return item

class Clause:
    contents = None
    awaitingNegation = None
    def __init__(self, contents, awaitingNegation=False):
        self.awaitingNegation = awaitingNegation
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
            if self.awaitingNegation:
                sign = not sign
            return Literal(symbol, sign)
        else:
            return self
    def toCNF(self):
        #Simple check to see if we are a literal
        literal = self.toLiteral()
        if isinstance(literal, Literal):
            return literal
        #Now we have more work to do
        #Convert all sub-clauses to CNF (yay recursion)
        newContents = list(map(lambda x:conversion(x),self.contents))
        #If we have only ANDs of CNF clauses, then we are done
        onlyAnds = all(map(lambda x: x==operators.AND, filter(lambda y: isinstance(y, operators), newContents)))
        if onlyAnds:
            return newContents
        


    def negate(self):
        self.awaitingNegation = not self.awaitingNegation

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





simpleLiteralClause = [Clause(['a']), Clause(['b'])]

