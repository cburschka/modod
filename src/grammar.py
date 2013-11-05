import tokens
import dre

class NonTerm:
    pass

class Nary(NonTerm):
    def __init__(self, production):
        _, expr1, _, expr2, remainder, _ = production
        self.children = [expr1, expr2] + remainder.children        

class NaryRep(NonTerm):
    def __init__(self, production):
        if production:
            print(production)
            _, expr, remainder = production
            self.children = [expr] + remainder.children
        else:
            self.children = []
    
class Concat(Nary):
    def dre(self):
        return dre.Concatenation([x.dre() for x in self.children])
        
class ConcatRep(NaryRep):
    pass

class Choice(Nary):
    def dre(self):
        return dre.Choice([x.dre() for x in self.children])

class ChoiceRep(NaryRep):
    pass

class Unary(NonTerm):
    def __init__(self, production):
        _, expr, _, _ = production
        self.child = expr

class Plus(Unary):
    def dre(self):
        return dre.Plus(self.child.dre())
        
class Opt(Unary):
    def dre(self):
        return dre.Optional(self.child.dre())

class Expr(NonTerm):
    def __init__(self, production):
        self.expr = production[0]

    def dre(self):
        if type(self.expr) is tokens.Terminal:
            return dre.Terminal(self.expr.symbol)
        return self.expr.dre()


terms = tokens.allTokens
nonterms = [Expr, Concat, ConcatRep, Choice, ChoiceRep, Plus, Opt]

start = Expr

productions = [(Expr, (x,)) for x in [Concat, Choice, Plus, Opt, tokens.Terminal]] + [
    (Concat, (tokens.LeftParen, Expr, tokens.Concat, Expr, ConcatRep, tokens.RightParen)),
    (Choice, (tokens.LeftParen, Expr, tokens.Choice, Expr, ChoiceRep, tokens.RightParen)),
    (Plus, (tokens.LeftParen, Expr, tokens.RightParen, tokens.Plus)),
    (Opt, (tokens.LeftParen, Expr, tokens.RightParen, tokens.Opt)),
    (ChoiceRep, (tokens.Choice, Expr, ChoiceRep)),
    (ChoiceRep, ()),
    (ConcatRep, (tokens.Concat, Expr, ConcatRep)),
    (ConcatRep, ())
]
