import string

# Der Lexer erkennt zwei Sorten Symbole:
#   - Beliebig viele Meta-Symbole, die aus je einem Character bestehen.
#     meta ist ein dictionary von Character zu Symbol.
#   - Genau ein Terminal-Symbol, das aus beliebigen Character bestehen kann,
#     aber keinen Whitespace und keine Meta-Zeichen enthält.
#
# Optional: char_filter (Character -> Bool), gibt aus, ob ein Character 
#     (der keinem Meta-Symbol zugeordnet ist) Teil eines Terminalsymbols sein 
#     darf. Tritt ein Character x auf, der weder Whitespace, noch Meta-Symbol,
#     noch erlaubtes Zeichen ist, so schlägt die lexikalische Analyse fehl.
#
#     Ohne char_filter werden alle Zeichen, die nicht Whitespace oder Meta-Symbol
#     sind, als Teil eines Terminalsymbols gelesen.
class lexer:
    def __init__(self, meta, terminal, char_filter=None):
        assert set(meta.keys()) & set(string.whitespace) == set(), 'Whitespace characters cannot be meta characters.'
        assert char_filter == None or not any(char_filter(x) for x in set(meta.keys()) | set(string.whitespace)), 'Whitespace and meta characters cannot be terminal characters'
        self.meta = meta
        self.terminal = terminal
        self.filter = char_filter

    def lex(self, s):
        tokens = []
        j = -1

        # Das Leerzeichen beendet ein Terminalsymbol am Ende des Inputs.
        s += ' '

        for i, c in enumerate(s):
            # Wird ein Meta- oder Whitespace-Zeichen gefunden:
            if c in self.meta or c in string.whitespace:
                # So beende ggf. das aktuelle Terminalsymbol
                if j >= 0:
                    tokens.append(self.terminal(s[j:i]))
                    j = -1
                # Füge das Meta-Symbol ein
                if c in self.meta:
                    tokens.append(self.meta[c]())
            # Wird ein erlaubtes Terminalzeichen gefunden:
            elif self.filter == None or self.filter(c):
                # So beginne ggf. ein neues Terminalsymbol
                if j < 0:
                    j = i
            else:
                raise LexError(i, c)

        return tokens
    
class LexError(ValueError):
    def __init__(self, i, c):
        self.i, self.c = i, c
    def __str__(self):
        return 'Lexical Error at #{}: {} is not allowed.'.format(self.i, self.c)

