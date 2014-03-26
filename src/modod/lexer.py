import string

# The lexer knows two classes of symbols:
#   - any number of meta-symbols, which match a single meta-character each.
#     this argument is a dictionary mapping meta-characters to symbol classes.
#
#   - exactly one terminal symbol, which matches a run of any characters
#     but ends as soon as a meta-character or a whitespace character
#     (not escaped with "\") is encountered.
#     whitespace characters delimit a sequence of multiple terminal symbols.
#
#     this argument is a single symbol class.
#
#   - optional: char_filter (character -> bool) determines if a character is
#     allowed in a terminal symbol. A character that neither matches a
#     meta-symbol, nor is whitespace, nor allowed in terminals, will cause the
#     lexical analysis to fail.
#
#   - optional: with letters=True, each terminal character becomes a terminal
#     symbol. This has the same effect as adding spaces between every character
#     of the input.
class lexer:
    def __init__(self, meta, terminal, char_filter=None, letters=False):
        assert not (set(meta.keys()) & set(string.whitespace)), 'Whitespace characters cannot be meta characters.'
        self.meta = meta
        self.terminal = terminal
        self.filter = char_filter
        self.letters = letters

    def lex(self, s):
        tokens = []
        term = ''  # The current terminal character run.
        bs = False # The last character was a backslash.

        # This space terminates a terminal symbol at the end of the input.
        s += ' '

        for i, c in enumerate(s):
            # We found an unescaped backslash.
            if not bs and c == '\\':
                bs = True
            # We found an unescaped meta or whitespace character.
            elif not bs and (c in self.meta or c in string.whitespace):
                # Append the current terminal symbol (if any):
                if term:
                    tokens.append(self.terminal(term))
                    term = ''
                # Append the meta symbol (if any):
                if c in self.meta:
                    tokens.append(self.meta[c]())
            # found another character, or one escaped by a backslash:
            elif self.filter == None or self.filter(c):
                bs = False
                # Append it to the current terminal symbol:
                term += c
                if self.letters:
                    # If terminals are single characters, append it immediately:
                    tokens.append(self.terminal(term))
                    term = ''
            else:
                raise LexError(i, c)

        return tokens

class LexError(ValueError):
    def __init__(self, i, c):
        self.i, self.c = i, c
    def __str__(self):
        return 'Lexical Error at #{}: {} is not allowed.'.format(self.i, self.c)

