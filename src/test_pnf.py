import modod
import graph

cases = [
   #format: input expected comment
   #if expected=='', no comparison is performed
   ['((a? | b?)? |(c? | d?)?)?','(a|b|c|d)?','4.1'],
   ['(a? b?)+','(a|b)+?','4.2'],
   ['(a?|(b?,c?))?','(a|(b?,c?))','4.3'],
   ['(((a1? | b1?)? |(c1? | d1?)?)?,((a2? | b2?)? |(c2? | d2?)?)?)+','',''],
   ['(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?','',''],
   ['(a*,b*)+','(a|b)+?',''],
   ['(((a?,b?)+,c*)+,d)','((a|b|c)+?,d)',''],
   ['(a*+?+?+?,b*+?+?+?)+','(a|b)+?',''],
]

problems = False

for ist,soll,desc in cases:
    print('============================')
    if desc!='':
        print(desc)
    try:
        tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre()
        print('Input:\n    ', tree_dre.toString())
        pnfIst = tree_dre.toNNF().toPNF().toString()

        print('PNF:\n    ', pnfIst)
        if soll!='':
            if (pnfIst==soll):
                print('OK')
            else:
                print('Not OK! (ಠ_ಠ). Expected:\n    ', soll)
                problems = True

    except ValueError as e:
        print('  Fehler:', e)

print('============================')
if problems:
    problems = True
    print('An error occurred.     (ಠ_ಠ)')
else:
    print('All is well.  ┏(-_-)┛┗(-_-)┓')