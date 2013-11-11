import grammar_extended as ge

lexer = ge.build_lexer()
grammar = ge.build_grammar()
parser = grammar.slr1()


def parse(s):
    tokens = lexer.lex(s)
    parsed = parser.parse(tokens, verbose=False)
    return parsed.dre()

for s in ['(((a)))', '(a? a,a* a+)', '(a(Test|Te)*b(c+))?', 'a|b c | ef d* (a b)?']:
    tree = parse(s)
    print('++++\n', s, '\nwird zu:\n', tree, '\nin kanonischer Form: ', tree.formula())

