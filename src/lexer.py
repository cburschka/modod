# Der Lexer erkennt zwei Sorten Symbole:
#   - Beliebig viele Meta-Symbole, die aus je einem Zeichen bestehen.
#     meta ist ein dictionary von Zeichen zu Token-Typ
#   - Genau ein Terminal-Symbol, das aus beliebigen Zeichen bestehen kann,
#     aber keinen Whitespace und keine Meta-Zeichen enthält.
class LexError(ValueError):
    def __init__(self, i, c):
        self.i, self.c = i, c
    def __str__(self):
        return 'Lexical Error at #{}: {} is not allowed.'.format(self.i, self.c)

class lexer:
    def __init__(self, meta, terminal, char_filter=None):
        self.meta = meta
        self.terminal = terminal
        self.filter = char_filter

    def lex(self, string):
        tokens = []
        j = -1

        for i, c in enumerate(string + ' '):
            if c in self.meta or isWhiteSpace(c):
                if j >= 0:
                    tokens.append(self.terminal(string[j:i]))
                    j = -1
                if c in self.meta:
                    tokens.append(self.meta[c]())
            elif self.filter == None or self.filter(c):
                if j < 0:
                    j = i
            else:
                raise LexError(i, c)

        return tokens


def isWhiteSpace(c):
    return c == ' ' or '\x09' <= c <= '\x0d'
