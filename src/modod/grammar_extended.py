from modod import grammar_strict as gs
from modod import tokens
from modod import dre
from parser.cfg import slr1_grammar
import parser.symbol
from modod import lexer

# Syntax extensions:
#   - Omission of Concatenation delimiter (,).
#   - * as a shortcut for +?
#   - character groups ("[" { x | x "-" x } "]") as a shortcut for Choice.
#   - Arbitrary omission or addition of parentheses, using operator precedence:
#     Unary >> Concatenation >> Choice

'''Unparenthesized unary symbol.'''
class Unary(gs.Unary):
    def child(self):
        return self.production[0]

'''Unparenthesized nary symbol.'''
class Nary(gs.Nary):
    def children(self):
        yield self.production[0]
        yield self.production[2]
        # TODO: Python 3.3+ has 'yield from'.
        for x in self.production[3].children():
            yield x

'''Parenthesized expression symbol'''
class Paren(gs.Expr):
    def dre(self):
        return self.production[1].dre()

'''Kleene Star'''
class OptPlus(Unary):
    def dre(self):
        return dre.Optional(dre.Plus(self.child().dre()))

# Through multiple inheritance, these operators override
# the child(), children() functions in the overridden strict operators.
class Optional(Unary, gs.Optional):
    pass
class Plus(Unary, gs.Plus):
    pass
class Concat(Nary, gs.Concat):
    pass
class Choice(Nary, gs.Choice):
    pass

# Optional comma delimiter.
class ConcatDelim(parser.symbol.NonTerm):
    pass

# Expr can have any form.
# Expr2 is the child of a Choice, so it cannot be a Choice.
# Expr3 is the child of a Concatenation or a unary, so it must be unary or parenthesized.
# A parenthesized expression can have any form again.
class Expr2(gs.Expr):
    pass
class Expr3(gs.Expr):
    pass

# * Terminal
class Star(parser.symbol.Term):
    pass
# [] Terminals for character groups.
class SquareOpen(parser.symbol.Term):
    pass
class SquareClose(parser.symbol.Term):
    pass
# Content of a character group
class TermRep(parser.symbol.NonTerm):
    def children(self):
        if self.production:
            yield self.production[0]
            for child in self.production[1].children():
                yield child

# Character group nonterm.
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
    # The actual productions of the grammar.
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
