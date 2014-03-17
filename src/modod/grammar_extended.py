from modod import grammar_strict as gs
from modod import tokens
from modod import dre
from parser.cfg import slr1_grammar
import parser.symbol
from modod import lexer

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
class ConcatDelim(parser.symbol.NonTerm):
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
class Star(parser.symbol.Term):
    pass

class SquareOpen(parser.symbol.Term):
    pass
class SquareClose(parser.symbol.Term):
    pass
class TermRep(parser.symbol.NonTerm):
    def children(self):
        if self.production:
            yield self.production[0]
            for child in self.production[1].children():
                yield child

class CharGroup(gs.Expr):
    def children(self):
        yield self.production[1]
        for child in self.production[2].children():
            yield child

    def dre(self):
        x = ''.join(x.symbol for x in self.children())
        z = []
        for i in range(1, len(x)-1):
            if x[i] == '-':
                z += [chr(a) for a in range(ord(x[i-1]), ord(x[i+1])+1)]
            else:
                z.append(x[i-1])
        if len(x) > 1 and x[-2] != '-':
            z += x[-2:]
        assert z, 'Empty character group.'
        return dre.Choice([dre.Terminal(a) for a in z])

def build_grammar():
    productions = {
        gs.Expr : {(Choice,), (Expr2,)},
        Expr2 : {(Concat,), (Expr3,)},
        Expr3 : {(Paren,), (Optional,), (Plus,), (OptPlus,), (gs.TermExpr,), (CharGroup,)},
        Paren : {(tokens.LeftParen, gs.Expr, tokens.RightParen),},
        Choice : {(Expr2, tokens.Pipe, Expr2, gs.ChoiceRep)},
        gs.ChoiceRep : {(tokens.Pipe, Expr2, gs.ChoiceRep), ()},
        Concat : {(Expr3, ConcatDelim, Expr3, gs.ConcatRep)},
        gs.ConcatRep : {(ConcatDelim, Expr3, gs.ConcatRep), ()},
        OptPlus : {(Expr3, Star)},
        CharGroup : {(SquareOpen, tokens.Terminal, TermRep, SquareClose)},
        TermRep : {(tokens.Terminal, TermRep), ()},
        Plus : {(Expr3, tokens.PlusSign)},
        Optional : {(Expr3, tokens.Question)},
        ConcatDelim : {(tokens.Comma,), ()},
        gs.TermExpr : {(tokens.Terminal,)}
    }

    return parser.cfg.slr1_grammar(productions, start=gs.Expr)

def build_lexer():
    table = tokens.table.copy()
    table['*'] = Star
    table['['] = SquareOpen
    table[']'] = SquareClose

    return lexer.lexer(table, tokens.Terminal)
