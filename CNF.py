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
    def toCNF(self):
        #Simple check to see if we are a literal
        if isinstance(self, Literal):
            return self
        #Now we have more work to do
        #Convert all sub-clauses to CNF (yay recursion)
        newContents = list(map(lambda x:conversion(x),self.contents))
        #If we have only ANDs of CNF clauses, then we are done
        onlyAnds = all(map(lambda x: x==operators.AND, filter(lambda y: isinstance(y, operators), newContents)))
        if onlyAnds:
            return  CNFClause(newContents)
        #If the statement is composed of only ORs of Literals, then we are done
        onlyOrs = all(map(lambda x: x==operators.OR, filter(lambda y: isinstance(y,operators), newContents)))
        onlyLiterals = all(map(lambda x: isinstance(x,Literal), filter(lambda y: isinstance(y,Clause), newContents)))
        if onlyOrs and onlyLiterals:
            return CNFClause(newContents)
        #Now we have to manipulate symbols
        unresolved = True
        while unresolved:
            unresolved = False
            for i in range(len(newContents)):
                cur = newContents[i]
                if isinstance(cur,operators):
                    unresolved = True
                    if cur == operators.NOT:
                        #The unary operator
                        newContents[i+1] = newContents[i+1].negate()
                        #We Processesed the negation, so remove it
                        newContents.pop(i)
                    else:
                        #Grab our operands
                        operands = [newContents.pop(i-1),newContents.pop(i+1)]



        #Conversion to CNF not possible
        raise TypeError


    def __str__(self):
        st = ""
        for i in self.contents:
            st += str(i)
        return st


    def negate(self):
        self.awaitingNegation = not self.awaitingNegation

negationDict = {
    operators.AND:operators.OR,
    operators.OR:operators.AND
}

def negationMapping(i):
    if isinstance(i,Clause):
        return i.negate()
    else:
        return negationDict[i]

class CNFClause(Clause):
    #A marked, valid clause in CNF
    def negate(self):
        self.contents = list(map(negationMapping, self.contents))


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
level = Clause([b,operators.OR,c])
topLevel = Clause([a,operators.AND,level])
print(topLevel.toCNF())

