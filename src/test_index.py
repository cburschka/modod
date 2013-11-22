import modod, graph
import modod.indexed_dre

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
    try:
        tree_dre = modod.DREfromString(s)
        tree_index = modod.indexed_dre.add_index(tree_dre)
        print('  Baum:\n    ', tree_dre)
        print('  Index-Baum:\n    ', tree_index)
        open('{}-indexed.dot'.format(i), 'w+').write(tree_index.toDOTString())
    except ValueError as e:
        print('  Fehler:', e)
