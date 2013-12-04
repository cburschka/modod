from . import grammar_extended
from . import grammar_strict
from . import dre_lexer
from . import dre_indexed
from . import oa

_lexerExt = grammar_extended.build_lexer()
_parserExt = grammar_extended.build_grammar().slr1()
_lexerStrict = dre_lexer.build_lexer()
_parserStrict = grammar_strict.build_grammar().slr1()

def DREfromString(string, strict=False):
    if strict:
        return _parserStrict.parse(_lexerStrict.lex(string)).dre()
    else:
        return _parserExt.parse(_lexerExt.lex(string)).dre()
    
def compareDREs(a, b):
    raise NotImplementedError() #TODO


# Pseudo-Constructors (shortcuts):
dre.DRE.fromString = DREfromString
oa.OA.fromString = lambda string : oa.OA.fromDRE(dre.DRE.fromString(string))
oa.OA.fromDRE = lambda tree : oa.OA.fromIndexedDRE(dre_indexed.IndexedDRE(tree))
oa.OA.fromIndexedDRE = lambda itree : oa.OA.fromIndexedNode(itree.root)

