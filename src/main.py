import cfg
import lexer
import sugar

lex = lexer.lexer(sugar.meta, sugar.terminal)
grammar = cfg.grammar(sugar.productions, sugar.start)
print(grammar)
parser = grammar.slr1()
print(parser)


def parse(s):
    tokens = lex.lex(s)
    parsed = parser.parse(tokens)
    #print(parsed)
    return parsed.dre()
    
for s in ['(((a)))', '(a? a,a* a+)', '(a(Test|Te)*b(c+))?']:
    tree = parse(s)
    print(s, 'wird zu: ', tree, ' in kanonischer Form: ', tree.formula())

