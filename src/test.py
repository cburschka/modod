import modod.grammar_strict as gs
import modod.grammar_extended as ge
import modod.dre_lexer as dre_lexer
import graph

strict = (dre_lexer.build_lexer(), gs.build_grammar().slr1())
extended = (ge.build_lexer(), ge.build_grammar().slr1())

cases = [
    '(((a)))',
    '(a? a,a* a+)',
    '(a(Test|Te)*b(c+))?',
    'a|b c | ef d* (a b)?',
    '(a+|a)'
]

for i,s in enumerate(cases):
    print('============================')
    print('Input:', s)
    for label, (lexer, parser) in (('strict', strict), ('extended', extended)):
        print('+++++++++++++++++++')
        print('Format:', label)
        try:

            chain = lexer.lex(s)
            print('  Kette:\n    ', ' '.join(map(str, chain)))
            tree = parser.parse(chain, verbose=False)
            tree_dre = tree.dre()
            print('  Baum:\n    ', tree_dre)
            canonical = tree_dre.formula()
            print('  Kanonische Form\n    ', canonical)
            print('  Eingabe = Kanonische Form?\n    ', ['Nein', 'Ja'][canonical == s])
            reparse = strict[1].parse(strict[0].lex(canonical)).dre().formula()
            print('  Kanonisch -> Strict -> Kanonisch:\n    ', reparse)
            print('  Kanonische Form ist Fixpunkt?\n    ', ['Nein', 'Ja'][canonical == reparse])
            nodes, edges = tree.graph()
            open('{}-{}-syntax.dot'.format(label, i), 'w+').write(graph.digraph(nodes, edges).xdot())
            nodes, edges = tree_dre.graph()
            open('{}-{}-dre.dot'.format(label, i), 'w+').write(graph.digraph(nodes, edges).xdot())
        except ValueError as e:
            print('  Fehler:', e)
