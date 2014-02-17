from . import grammar_extended
from . import grammar_strict
from . import dre_lexer
from . import dre_indexed
from . import dre_factor
from . import dre_rewritep
from . import oa

# Compile the parsers (these should not be used directly outside of unit tests, normally)
_lexerExt = grammar_extended.build_lexer()
_parserExt = grammar_extended.build_grammar().slr1()
_lexerStrict = dre_lexer.build_lexer()
_parserStrict = grammar_strict.build_grammar().slr1()

CHARGROUP_NONE = 0
CHARGROUP_COMPLETE = 1
CHARGROUP_PARTIAL = 2

charGroup = CHARGROUP_COMPLETE

# Parsing function
def DREfromString(string, strict=False):
    if strict:
        return _parserStrict.parse(_lexerStrict.lex(string)).dre()
    else:
        return _parserExt.parse(_lexerExt.lex(string)).dre()

def _DRE_simplify(rho):
    old, new = None, rho
    while old != new:
        old, new = new, new.factorOut().rewritePlus().toPNF()
    return new

# Raise comparators to main module namespace (cf. specification)
equivalentToMEW = oa.OA.equivalentToMEW
equivalentTo = oa.OA.equivalentTo

# Pseudo-Constructor shortcuts (cf. specification):
dre.DRE.fromString = DREfromString
oa.OA.fromString = lambda string : oa.OA.fromDRE(dre.DRE.fromString(string))
oa.OA.fromDRE = lambda tree : oa.OA.fromIndexedDRE(dre_indexed.IndexedDRE.fromDRE(tree))

# Attach submodule functions to DRE class:

dre.DRE.rewritePlus = dre_rewritep.rewritePlus
dre.DRE.factorOut = dre_factor.factorOut
dre.DRE.equivalentTo = lambda a, b: oa.OA.fromDRE(a).equivalentTo(oa.OA.fromDRE(b))
dre.DRE.simplify = _DRE_simplify
