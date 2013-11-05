import tokens

def lex(s):
    tokenList = []
    j = -1
    
    for i,c in enumerate(s + ' '):
        if not isTerminalCharacter(c):
            if j >= 0:
                tokenList.append(tokens.Terminal(s[j:i]))
                j = -1
            if isMetaCharacter(c):
                tokenList.append(readToken(c))
        elif j < 0:
            j = i

    return tokenList

def isTerminalCharacter(c):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9')
    
def isMetaCharacter(c):
    return c in ('(', ')', '|', ',', '?', '+')

def readToken(c):
    if c == '(':
        return tokens.LeftParen()
    elif c == ')':
        return tokens.RightParen()
    elif c == '+':
        return tokens.Plus()
    elif c == '?':
        return tokens.Opt()
    elif c == '|':
        return tokens.Choice()
    elif c == ',':
        return tokens.Concat()

