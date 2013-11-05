class Token:
    def __str__(self):
        return self.__class__.__name__
    
class Terminal(Token):
    def __init__(self, symbol):
        self.symbol = symbol
    def __str__(self):
        return 'Terminal("{0}")'.format(self.symbol)

class LeftParen(Token):
    def __str__(self):
        return "LeftParen"

class RightParen(Token):
    def __str__(self):
        return "RightParen"
    
class Concat(Token):
    pass
    
class Choice(Token):
    pass
    
class Plus(Token):
    pass
    
class Question(Token):
    pass
    

