from . import grammar_extended
from . import grammar_strict
from . import dre_lexer
from . import dre_indexed
from . import occurrence_automaton

_lexerExt = grammar_extended.build_lexer()
_parserExt = grammar_extended.build_grammar().slr1()
_lexerStrict = dre_lexer.build_lexer()
_parserStrict = grammar_strict.build_grammar().slr1()

def DREfromString(string, strict=False):
    if strict:
        return _parserStrict.parse(_lexerStrict.lex(string)).dre()
    else:
        return _parserExt.parse(_lexerExt.lex(string)).dre()

def IndexedDREfromDRE(dre):
    return dre_indexed.IndexedDRE(dre)
    
def OAfromIndexedDRE(idre):
    return occurrence_automaton.OAfromIndexedDRE(idre)

def compareDREs(a, b):
    raise NotImplementedError() #TODO

