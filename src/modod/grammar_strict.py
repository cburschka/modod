from . import tokens
from . import dre
import parser.cfg
from parser.symbol import NonTerm

class Nary(NonTerm):
    def children(self):
        yield self.production[1]
        yield self.production[3]
        # TODO: Python 3.3+ erlaubt 'yield from'.
        for x in self.production[4].children():
            yield x
    def dre(self):
        return self.dre_type()([x.dre() for x in self.children()])

class NaryRep(NonTerm):
    def children(self):
        if self.production:
            yield self.production[1]
            for x in self.production[2].children():
                yield x

class Unary(NonTerm):
    def child(self):
        return self.production[0]
    def dre(self):
        return self.dre_type()(self.child().dre())

class Concat(Nary):
    def dre_type(self):
        return dre.Concatenation
class ConcatRep(NaryRep):
    pass

class Choice(Nary):
    def dre_type(self):
        return dre.Choice
class ChoiceRep(NaryRep):
    pass

class Plus(Unary):
    def dre_type(self):
        return dre.Plus

class Optional(Unary):
    def dre_type(self):
        return dre.Optional

class TermExpr(NonTerm):
    def dre(self):
        return dre.Terminal(self.production[0].symbol)

class Expr(NonTerm):
    def dre(self):
        return self.production[0].dre()

def build_grammar():
    productions = { Expr : {(Concat,), (Choice,), (Plus,), (Optional,), (TermExpr,)},
        Concat : {(tokens.LeftParen, Expr, tokens.Comma, Expr, ConcatRep, tokens.RightParen)},
        Choice : {(tokens.LeftParen, Expr, tokens.Pipe, Expr, ChoiceRep, tokens.RightParen)},
        Plus : {(Expr, tokens.PlusSign)},
        Optional : {(Expr, tokens.Question)},
        ChoiceRep : {(tokens.Pipe, Expr, ChoiceRep), ()},
        ConcatRep : {(tokens.Comma, Expr, ConcatRep), ()},
        TermExpr : {(tokens.Terminal,)}
    }

    return parser.cfg.slr1_grammar(productions, start=Expr)
