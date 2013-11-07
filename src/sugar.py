import grammar
import tokens
import dre

# Erlaubt:
#   - Klammern an beliebiger Stelle, dafür unäre Operatoren ohne Klammer.
#   - Konkatenieren ohne Komma
#   - Stern

class OptPlus(grammar.Unary):
    def dre(self):
        return dre.Optional(dre.Plus(self.child.dre()))

class Paren(grammar.Unary):
    def __init__(self, production):
        _, expr, _ = production
        self.expr = expr
    def dre(self):
        return self.expr.dre()


class Star(tokens.Token):
    pass


# Erweitert die Werte aus grammar und tokens entsprechend:


productions = grammar.productions.union([
    (grammar.Expr, (OptPlus,)),
    (grammar.Expr, (Paren,)),
    (Paren, (tokens.LeftParen, grammar.Expr, tokens.RightParen)),
    (grammar.Concat, (tokens.LeftParen, grammar.Expr, grammar.Expr, grammar.ConcatRep, tokens.RightParen)),
    (grammar.ConcatRep, (grammar.Expr, grammar.ConcatRep)),
    (OptPlus, (grammar.Expr, Star)),
    (grammar.Plus, (grammar.Expr, tokens.Plus)),
    (grammar.Opt, (grammar.Expr, tokens.Question))
]).difference([
    (grammar.Plus, (tokens.LeftParen, grammar.Expr, tokens.RightParen, tokens.Plus)),
    (grammar.Opt, (tokens.LeftParen, grammar.Expr, tokens.RightParen, tokens.Question)),
])



start = grammar.start

meta = tokens.meta.copy()
meta['*'] = Star
terminal = tokens.terminal
