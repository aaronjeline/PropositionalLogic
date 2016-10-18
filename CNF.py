from enum import Enum
class Literal:
    symbol = None
    sign = None
    def __init__(self, symbol, sign=True):
        self.symbol = symbol
        self.sign =sign

    def negate(self):
        return Literal(self.symbol, not self.sign)

class Clause:
    contents = None
    def __init__(self, contents):
        self.contents = contents

class operators(Enum):
    AND = 0
    OR = 1
    NOT = 2
    IMPLIES = 3
    EQUALS = 4

def toCNF(phrase):
    #Reduce all sub-clauses to CNF
    clauses = filter(lambda x: isinstance(x, Clause), phrase)
    clauses = list(map(lambda x:toCNF(x), clauses))
    for i in phrase:
        if isinstance(i, Clause):
            phrase[phrase.index(i)] = clauses.pop(0)

