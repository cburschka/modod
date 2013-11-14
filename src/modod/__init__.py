from . import grammar_extended

lexer = grammar_extended.build_lexer()
parser = grammar_extended.build_grammar().slr1()

def parse(string):
    return parser.parse(lexer.lex(string)).dre()
    
def nnf(dre):
    return dre.nary_normal_form()
    
def write(dre):
    return dre.formula()
