class Literal:
    symbol = None
    sign = None
    def __init__(self, symbol, sign=True):
        self.symbol = symbol
        self.sign =sign

    def negate(self):
        return Literal(self.symbol, not self.sign)

