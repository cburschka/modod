import modod
from graph import graph

cases = [
    '(((a)))',
    '(a? a,a* a+)',
    '(a(Test|Te)*b(c+))?',
    'a|b c | ef d* (a b)?',
    '(a+|a)'
]

strict = (modod._lexerStrict, modod._parserStrict)
extended = (modod._lexerExt, modod._parserExt)

for i,s in enumerate(cases):
    print('============================')
    print('Input:', s)
    for label, (l, p) in (('strict', strict), ('extended', extended)):
        print('+++++++++++++++++++')
        print('Format:', label)
        try:
            chain = l.lex(s)
            print('  Kette:\n    ', ' '.join(map(str, chain)))
            tree = p.parse(chain, verbose=False)
            tree_dre = tree.dre()
            print('  Baum:\n    ', tree_dre)
            canonical = tree_dre.toString()
            print('  Kanonische Form\n    ', canonical)
            print('  Eingabe = Kanonische Form?\n    ', ['Nein', 'Ja'][canonical == s])
            reparse = strict[1].parse(strict[0].lex(canonical)).dre().toString()
            print('  Kanonisch -> Strict -> Kanonisch:\n    ', reparse)
            print('  Kanonische Form ist Fixpunkt?\n    ', ['Nein', 'Ja'][canonical == reparse])
            nodes, edges = tree.graph()
            open('{}-{}-syntax.dot'.format(label, i), 'w+').write(graph.digraph(nodes, edges).xdot())
            open('{}-{}-dre.dot'.format(label, i), 'w+').write(tree_dre.toDOTString())
        except ValueError as e:
            print('  Fehler:', e)
