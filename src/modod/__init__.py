from . import grammar_extended
from . import grammar_strict
from . import dre_lexer

_lexerExt = grammar_extended.build_lexer()
_parserExt = grammar_extended.build_grammar().slr1()
_lexerStrict = dre_lexer.build_lexer()
_parserStrict = grammar_strict.build_grammar().slr1()

def DREfromstring(string, strict=False):
    if strict:
        return _parserStrict.parse(_lexerStrict.lex(string)).dre()
    else:
        return _parserExt.parse(_lexerExt.lex(string)).dre()

def compareDREs(a, b):
    raise NotImplementedError() #TODO

