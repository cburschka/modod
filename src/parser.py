import grammar
import cfg

ll1parser = cfg.ll1(grammar.terms, grammar.nonterms, grammar.productions, grammar.start)

def parse(s):
    return ll1parser.parse(s)

#print(ll1parser)
