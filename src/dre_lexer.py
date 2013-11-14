import lexer
import tokens

def allowed_character(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9' or c == '_'

def build_lexer():
    return lexer.lexer(tokens.table, tokens.Terminal, allowed_character)
