import modod
import graph

cases = [
   ['((a? | b?)? |(c? | d?)?)?','(a|b|c|d)?','4.1'],
   ['(a? b?)+','(a|b)+?','4.2'],
   ['(a?|(b?,c?))?','(a|(b?,c?))','4.3']
]

problems = False

for ist,soll,desc in cases:
    print('============================')
    if desc!='':
        print(desc)
    print('Input:', ist)
    try:
        chain = modod._lexerExt.lex(ist)
        tree = modod._parserExt.parse(chain, verbose=False)
        tree_dre = tree.dre()
        canonical = tree_dre.toString()
        reparse = modod._parserStrict.parse(modod._lexerStrict.lex(canonical)).dre().toString()
 
        pnfIst = tree_dre.toNNF().toPNF().toString()

        print('PNF:\n    ', pnfIst)
        print('Expected:\n    ', soll)
        if (pnfIst==soll):
            print(' OK')
        else:
            print('Not OK! (ಠ_ಠ)')
            problems = True

    except ValueError as e:
        print('  Fehler:', e)

print('============================')
if problems:
    problems = True
    print('An error occurred. (ಠ_ಠ)')
else:
    print('All is well. ┏(-_-)┛┗(-_-﻿ )┓ ')