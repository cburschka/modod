import grammar_strict as gs
import tokens
import dre
import cfg
import lexer

# Erweiterungen:
#   - Konkatenation ohne Komma
#   - * statt +?
#   - Beliebiges Auslassen oder Hinzufügen von Klammern, unter der folgenden
#     Operatorenpräzedenz:  Unär >> Konkatenation >> Auswahl

'''Ungeklammertes unary-Symbol.'''
class Unary(gs.Unary):
    def child(self):
        return self.production[0]

'''Ungeklammertes nary-Symbol.'''
class Nary(gs.Nary):
    def children(self):
        yield self.production[0]
        yield self.production[2]
        # TODO: Python 3.3+ erlaubt 'yield from'.
        for x in self.production[3].children():
            yield x

'''Klammerausdruck'''
class Paren(gs.Expr):
    def dre(self):
        return self.production[1].dre()

'''Sternausdruck'''
class OptPlus(Unary):
    def dre(self):
        return dre.Optional(dre.Plus(self.child().dre()))

# Durch Mehrfachvererbung überschreiben diese Operatoren in den strikten
# Operatoren nur die child() bzw. children() Funktion.
class Optional(Unary, gs.Optional):
    pass
class Plus(Unary, gs.Plus):
    pass
class Concat(Nary, gs.Concat):
    pass
class Choice(Nary, gs.Choice):
    pass

# Optionaler Komma-Delimiter.
class ConcatDelim(cfg.NonTerm):
    pass

# Expr kann jede Form haben.
# Expr2 ist innerhalb eines Choice-Ausdrucks und kann selbst kein Choice sein.
# Expr3 ist innerhalb einer Konkatenation oder einem unären Ausdruck und kann nur geklammert oder unär sein.
# Innerhalb einer Klammer steht wiederum ein beliebiger Expr-Ausdruck.
class Expr2(gs.Expr):
    pass
class Expr3(gs.Expr):
    pass

# *-Nichtterminal
class Star(tokens.Token):
    pass

def build_grammar():
    productions = {
        gs.Expr : {(Choice,), (Expr2,)},
        Expr2 : {(Concat,), (Expr3,)},
        Expr3 : {(Paren,), (Optional,), (Plus,), (OptPlus,), (gs.TermExpr,)},
        Paren : {(tokens.LeftParen, gs.Expr, tokens.RightParen),},
        Choice : {(Expr2, tokens.Pipe, Expr2, gs.ChoiceRep)},
        gs.ChoiceRep : {(tokens.Pipe, Expr2, gs.ChoiceRep), ()},
        Concat : {(Expr3, ConcatDelim, Expr3, gs.ConcatRep)},
        gs.ConcatRep : {(ConcatDelim, Expr3, gs.ConcatRep), ()},
        OptPlus : {(Expr3, Star)},
        Plus : {(Expr3, tokens.PlusSign)},
        Optional : {(Expr3, tokens.Question)},
        ConcatDelim : {(tokens.Comma,), ()},
        gs.TermExpr : {(tokens.Terminal,)}
    }

    return cfg.grammar(productions, start=gs.Expr)

def build_lexer():
    meta = tokens.meta.copy()
    meta['*'] = Star

    return lexer.lexer(meta, tokens.Terminal)
