from parser.symbol import Term

# These are the terminal symbols of the strict DRE grammar.

# The terminal symbol in the grammar of DREs
# which represents a terminal symbol of the parsed regular expression.
class Terminal(Term):
    def __init__(self, symbol):
        self.symbol = symbol
    def __str__(self):
        return 'Terminal("{0}")'.format(self.symbol)

class LeftParen(Term):
    pass

class RightParen(Term):
    pass

class Comma(Term):
    pass

class Pipe(Term):
    pass

class PlusSign(Term):
    pass

class Question(Term):
    pass

table = {
    '(' : LeftParen,
    ')' : RightParen,
    ',' : Comma,
    '|' : Pipe,
    '+' : PlusSign,
    '?' : Question
}
