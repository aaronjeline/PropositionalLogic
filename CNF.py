from enum import Enum


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

    def simpleCNFCheck(self,cnts):
        isCNF = False
        onlyAnds = all(map(lambda x: x==operators.AND, filter(lambda y: isinstance(y, operators), cnts)))
        onlyOrs = all(map(lambda x: x==operators.OR, filter(lambda y: isinstance(y, operators), cnts)))
        onlyLiterals = all(map(lambda x: isinstance(x, Literal), filter(lambda y: isinstance(y,Clause), cnts)))
        return onlyAnds or (onlyOrs and onlyLiterals)

    def toCNF(self):
        #Simple check to see if we are a literal
        if isinstance(self, Literal):
            return self
        #Now we have more work to do
        #Convert all sub-clauses to CNF (yay recursion)
        newContents = list(map(lambda x:conversion(x),self.contents))
        if self.simpleCNFCheck(newContents):
            return CNFClause(newContents)
        #Now we have to manipulate symbols
        #First eliminate all negations
        done = False
        while not done:
            try:
                #Get the next not
                i = newContents.index(operators.NOT)
                newContents[i+1] = newContents[i+1].negate()
                newContents.pop(i)
            except ValueError:
                #No more nots
                done = True
        if not self.simpleCNFCheck(newContents):
            #We have more resolution to do!
            pass
        #Done!
        return CNFClause(newContents)





    def __str__(self):
        st = ""
        for i in self.contents:
            if isinstance(i, Clause) and not isinstance(i, Literal):
                t = "(" + str(i) + ")"
                st += t
            else:
                st += str(i)
        return st


    def negate(self):
        self.awaitingNegation = not self.awaitingNegation

negationDict = {
    operators.AND:operators.OR,
    operators.OR:operators.AND
}

def negationMapping(i):
    if isinstance(i,CNFClause):
        return i.negate()
    else:
        return negationDict[i]

class CNFClause(Clause):
    #A marked, valid clause in CNF
    def negate(self):
        return Clause(list(map(negationMapping, self.contents))).toCNF()

    def toCNF(self):
        return self


class Literal(CNFClause):
    symbol = None
    sign = None
    def __init__(self, symbol, sign=True):
        self.symbol = symbol
        self.sign =sign

    def negate(self):
        return Literal(self.symbol, not self.sign)

    def __str__(self):
        if self.sign:
            return self.symbol
        else:
            return '-' + self.symbol

a = Literal('a')
b = Literal('b')
c = Literal('c')
k = Clause([b, operators.AND, c])
level = Clause([a, operators.AND, operators.NOT, k])
print(level.toCNF())
