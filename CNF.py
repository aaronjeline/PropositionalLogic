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
        # Strip all not's out of the contents, keep them in a seperate list
        nots = list(filter(lambda x: x == operators.NOT, self.contents))
        newContents = list(filter(lambda x: x not in nots, self.contents))
        # If there is more than one String left, it's not a literal
        if (len(newContents) == 1) and (isinstance(newContents[0], str)):
            # It's a literal
            symbol = newContents[0]
            sign = len(nots) % 2 == 0
            if self.awaitingNegation:
                sign = not sign
            return Literal(symbol, sign)
        else:
            return self

    def only(self, thing, type, list=None):
        if list == None:
            list = self.contents
        return all(map(lambda x: x==thing, filter(lambda y: isinstance(y,type), list)))

    def simpleCNFCheck(self, cnts):
        isCNF = False
        onlyAnds = self.only(operators.AND, operators, cnts)
        onlyOrs = self.only(operators.OR, operators, cnts)
        onlyLiterals = all(map(lambda x: isinstance(x, Literal), filter(lambda y: isinstance(y, Clause), cnts)))
        return onlyAnds or (onlyOrs and onlyLiterals)

    def resolveEquivalence(self, cnts):
        done = False
        while not done:
            try:
                i = cnts.index(operators.EQUALS)
                operands = [cnts.pop(i - 1) for e in range(3)]
                operands.pop(1)
                newClauses = []
                newClauses.append(Clause([operands[0], operators.IMPLIES, operands[1]]))
                newClauses.append(operators.AND)
                newClauses.append(Clause([operands[1], operators.IMPLIES, operands[0]]))
                cnts.insert(i, Clause(newClauses).toCNF())
            except ValueError:
                done = True
        return cnts

    def resolveImplies(self, cnts):
        done = False
        while not done:
            try:
                i = cnts.index(operators.IMPLIES)
                # Grab the operands and remove the operator
                operands = [cnts.pop(i - 1) for e in range(3)]
                operands.pop(1)
                newClause = Clause([operands[0].negate(), operators.OR, operands[1]]).toCNF()
                cnts.insert(i, newClause)
            except ValueError:
                # No more implies
                done = True
        return cnts

    def isAssociable(self):
        return self.only(operators.OR, operators)

    def distributeOr(self, cnts):
        done = False
        try:
            i = cnts.index(operators.OR)
            operands = [cnts.pop(i - 1) for e in range(3)]
            operands.pop(1)
            for i in range(2):
                if operands[1].isAssociable():
                    new = [operands[0], operators.OR]
                    if isinstance(operands[1], Literal):
                        new.append(operands[1])
                    else:
                        new.extend(operands[1].contents)
                    cnts[i:i] = new
                else:
                    #We need to actually distribute
                    clauses = filter(lambda x: isinstance(x, CNFClause), operands[1].contents)
                    newClause = []
                    for i in clauses:
                        newClause.append(Clause([operands[0], operators.OR, i]).toCNF())
                        newClause.append(operators.AND)
                    #Remove the last AND
                    newClause.pop()
                    cnts.insert(i, Clause(newClause).toCNF())
                #Flip the operands and do it again!
                operands = operands[::-1]
        except ValueError:
            pass
        return cnts


    def resolveNegations(self, cnts):
        done = False
        while not done:
            try:
                # Get the next not
                i = cnts.index(operators.NOT)
                cnts[i + 1] = cnts[i + 1].negate()
                cnts.pop(i)
            except ValueError:
                # No more nots
                done = True
        return cnts

    def toCNF(self):
        # Simple check to see if we are a literal
        if isinstance(self, Literal):
            return self
        # Now we have more work to do
        # Convert all sub-clauses to CNF (yay recursion)
        newContents = list(map(lambda x: conversion(x), self.contents))
        if self.simpleCNFCheck(newContents):
            return CNFClause(newContents)
        # Now we have to manipulate symbols
        newContents = self.resolveImplies(self.resolveEquivalence(self.resolveNegations(newContents)))

        while not self.simpleCNFCheck(newContents):
            newContents = self.distributeOr(newContents)

        # Done!
        return CNFClause(newContents)

    def __str__(self):
        st = ""
        for i in self.contents:
            if isinstance(i, Clause) and not isinstance(i, Literal):
                t = "(" + str(i) + ")"
                st += t
            else:
                st += str(i)
            st += " "
        return st

    def negate(self):
        self.awaitingNegation = not self.awaitingNegation


negationDict = {
    operators.AND: operators.OR,
    operators.OR: operators.AND
}


def negationMapping(i):
    if isinstance(i, CNFClause):
        return i.negate()
    else:
        return negationDict[i]


class CNFClause(Clause):
    # A marked, valid clause in CNF
    def negate(self):
        return Clause(list(map(negationMapping, self.contents))).toCNF()

    def toCNF(self):
        return self




class Literal(CNFClause):
    symbol = None
    sign = None
    contents = None

    def __init__(self, symbol, sign=True):
        self.symbol = symbol
        self.sign = sign
        self.contents = self

    def negate(self):
        return Literal(self.symbol, not self.sign)

    def isAssociable(self):
        return True

    def __str__(self):
        if self.sign:
            return self.symbol
        else:
            return '-' + self.symbol


a = Literal('a')
b = Literal('b')
c = Literal('c')
low = Clause([b, operators.OR, c])
high = Clause([a, operators.EQUALS, low])
print(high.toCNF())
