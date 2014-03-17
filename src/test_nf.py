import modod
from graph import graph

cases = [
    '(a|(a|b),b,(b c(b|af)))',
]

for i,s in enumerate(cases):
    print('============================')
    print('Input:', s)
    try:
        chain = modod._lexerExt.lex(s)
        print('  Kette:\n    ', ' '.join(map(str, chain)))
        tree = modod._parserExt.parse(chain, verbose=False)
        tree_dre = tree.dre()
        print('  Baum:\n    ', tree_dre)
        canonical = tree_dre.toString()
        print('  Kanonische Form\n    ', canonical)
        print('  Eingabe = Kanonische Form?\n    ', ['Nein', 'Ja'][canonical == s])
        reparse = modod._parserStrict.parse(modod._lexerStrict.lex(canonical)).dre().toString()
        print('  Kanonisch -> Strict -> Kanonisch:\n    ', reparse)
        print('  Kanonische Form ist Fixpunkt?\n    ', ['Nein', 'Ja'][canonical == reparse])

        nf = tree_dre.toNNF()

        print('  Normalform:\n    ', nf)
        print('  Normalform kanonisch:\n    ', nf.toString())

        open('nftest-{}.dot'.format(i), 'w+').write(tree_dre.toDOTString())
        open('nftest-{}-nf.dot'.format(i), 'w+').write(nf.toDOTString())
    except ValueError as e:
        print('  Fehler:', e)
