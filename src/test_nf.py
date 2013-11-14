import grammar_extended as ge
import graph

lexer, parser = ge.build_lexer(), ge.build_grammar().slr1()

cases = [
    '(a|(a|b),b,(b c(b|af)))',
]

for i,s in enumerate(cases):
    print('============================')
    print('Input:', s)
    try:
        chain = lexer.lex(s)
        print('  Kette:\n    ', ' '.join(map(str, chain)))
        tree = parser.parse(chain, verbose=False)
        tree_dre = tree.dre()
        print('  Baum:\n    ', tree_dre)
        canonical = tree_dre.formula()
        print('  Kanonische Form\n    ', canonical)
        print('  Eingabe = Kanonische Form?\n    ', ['Nein', 'Ja'][canonical == s])
        reparse = parser.parse(lexer.lex(canonical)).dre().formula()
        print('  Kanonisch -> Strict -> Kanonisch:\n    ', reparse)
        print('  Kanonische Form ist Fixpunkt?\n    ', ['Nein', 'Ja'][canonical == reparse])
        
        nf = tree_dre.nary_normal_form()
        
        print('  Normalform:\n    ', nf)
        print('  Normalform kanonisch:\n    ', nf.formula())
        
        nodes, edges = tree_dre.graph()
        open('nftest-{}.dot'.format(i), 'w+').write(graph.digraph(nodes, edges).xdot())
        nodes, edges = nf.graph()
        open('nftest-{}-nf.dot'.format(i), 'w+').write(graph.digraph(nodes, edges).xdot())
    except ValueError as e:
        print('  Fehler:', e)
