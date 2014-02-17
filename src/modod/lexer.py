import string

# Der Lexer erkennt zwei Sorten Symbole:
#   - Beliebig viele Meta-Symbole, die aus je einem Zeichen bestehen.
#     meta ist ein dictionary von Character zu Symbol.
#   - Genau ein Terminal-Symbol, das aus beliebigen Zeichen bestehen kann.
#     Whitespace und Metazeichen beenden ein Terminal-Symbol, wenn sie nicht
#     einem "\" folgen.
#
# Optional: char_filter (Character -> Bool), gibt aus, ob ein Zeichen
#     (der keinem Meta-Symbol zugeordnet ist) Teil eines Terminalsymbols sein
#     darf. Tritt ein Zeichen x auf, das weder Whitespace, noch Meta-Symbol,
#     noch erlaubtes Zeichen ist, so schlägt die lexikalische Analyse fehl.
#
#     Ohne char_filter werden alle Zeichen, die nicht Whitespace oder Meta-Symbol
#     sind, und nicht einem "\" folgen, als Teil eines Terminalsymbols gelesen.
class lexer:
    def __init__(self, meta, terminal, char_filter=None):
        assert not (set(meta.keys()) & set(string.whitespace)), 'Whitespace characters cannot be meta characters.'
        self.meta = meta
        self.terminal = terminal
        self.filter = char_filter

    def lex(self, s):
        tokens = []
        term = ''
        bs = False

        # Das Leerzeichen beendet ein Terminalsymbol am Ende des Inputs.
        s += ' '

        for i, c in enumerate(s):
            # Wird ein Meta- oder Whitespace-Zeichen gefunden:
            if not bs and c == '\\':
                bs = True
            elif not bs and (c in self.meta or c in string.whitespace):
                # So beende ggf. das aktuelle Terminalsymbol
                if term:
                    tokens.append(self.terminal(term))
                    term = ''
                # Füge das Meta-Symbol ein
                if c in self.meta:
                    tokens.append(self.meta[c]())
            # Wird ein erlaubtes Terminalzeichen gefunden:
            elif self.filter == None or self.filter(c):
                bs = False
                # So füge es dem aktuellen Terminalsymbol hinzu.
                term += c
            else:
                raise LexError(i, c)

        return tokens

class LexError(ValueError):
    def __init__(self, i, c):
        self.i, self.c = i, c
    def __str__(self):
        return 'Lexical Error at #{}: {} is not allowed.'.format(self.i, self.c)

