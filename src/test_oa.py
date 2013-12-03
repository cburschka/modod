import modod
import graph

cases = [
   '((a? | b?)? |(c? | d?)?)?',
   '(a? b?)+',
   '(a?|(b?,c?))?',
   '(((a1? | b1?)? |(c1? | d1?)?)?,((a2? | b2?)? |(c2? | d2?)?)?)+',
   '(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?',
   '(a*,b*)+',
   '(((a?,b?)+,c*)+,d)',
   '(a*+?+?+?,b*+?+?+?)+'
]

for i, case in enumerate(cases):
    print('============================')
    try:
        dre = modod.DREfromString(case)
        idre = modod.IndexedDREfromDRE(dre)
        oa = modod.OAfromIndexedDRE(idre)
        print('Input:\n    ', dre.toString())
        open('test_oa.{}.dot'.format(i), 'w').write(oa.graph().xdot())

    except ValueError as e:
        print('  Fehler:', e)

print('============================')

