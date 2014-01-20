import unittest

from modod.dre import DRE
from modod.oa import OA
from modod import equivalentTo, equivalentToMEW

class TestUM(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_pnf_example_4_1(self):
        self.assertEqual(DRE.fromString('((a? | b?)? |(c? | d?)?)?').toNNF().toPNF().toString(),'(a|b|c|d)?')
        
    def test_pnf_example_4_2(self):
        self.assertEqual(DRE.fromString('(a? b?)+').toNNF().toPNF().toString(),'(a|b)+?')

    def test_pnf_example_4_3(self):
        self.assertEqual(DRE.fromString('(a?|(b?,c?))?').toNNF().toPNF().toString(),'(a|(b?,c?))')

    def test_pnf_extra_1(self):
        ist='(a*,b*)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),'(a|b)+?')

    def test_pnf_extra_2(self):
        self.assertEqual(DRE.fromString('(((a?,b?)+,c*)+,d)').toNNF().toPNF().toString(),'((a|b|c)+?,d)')

    def test_pnf_extra_3(self):
        self.assertEqual(DRE.fromString('(a*+?+?+?,b*+?+?+?)+').toNNF().toPNF().toString(),'(a|b)+?')

    def test_pnf_extra_4(self):
        ist='(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)+?')

    def test_pnf_extra_5(self):
        ist='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)?')

    def test_pnf_extra_6(self):
        ist='(a?,b?,c+,d?)+'
        soll='(a?,b?,c,d?)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_extra_7(self):
        ist='(a?,b+)+'
        soll='(a?,b)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_extra_8(self):
        ist='(a+,b?)+'
        soll='(a,b?)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_extra_9(self):
        ist='(a?,b+,c+)+'
        soll='(a?,b+,c+)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_extra_10(self):
        ist='(a?,(b+|c+),d?)+'
        soll='(a?,(b|c),d?)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_extra_11(self):
        ist='(a?,(b+|(c?,d+)),e?)+'
        soll='(a?,(b|(c?,d)),e?)+'
        self.assertEqual(DRE.fromString(ist).toNNF().toPNF().toString(),soll)

    def test_pnf_no_side_effects(self):
        rx='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
        pnfrx=DRE.fromString(rx).toNNF().toPNF()
        self.assertEqual(pnfrx.toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)?')
        self.assertEqual(rx,'(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?')

    def test_pnf_extra_12(self):
        rx='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
        pnfnnfrx=DRE.fromString(rx).toNNF().toPNF()
        pnfrx=DRE.fromString(rx).toPNF()
        self.assertEqual(pnfnnfrx,pnfrx)

    def test_determinism_1(self):
        rxstr = 'a+'
        A = OA.fromString(rxstr)
        self.assertTrue(A.isDeterministic())

    def test_determinism_2(self):
        rxstr = '(a)*a'
        A = OA.fromString(rxstr)
        self.assertFalse(A.isDeterministic())

    def test_determinism_3(self):
        rxstr = '(a,b)|(a,c)'
        A = OA.fromString(rxstr)
        self.assertFalse(A.isDeterministic())

    def test_determinism_4(self):
        rxstr = 'a a a a'
        A = OA.fromString(rxstr)
        self.assertTrue(A.isDeterministic())

    def test_determinism_5(self):
        rxstr = '(ab)|(ac)'
        A = OA.fromString(rxstr)
        self.assertTrue(A.isDeterministic())

    def test_determinism_6(self):
        A=OA.fromString('(a,(a,(a,(a,(a,(a,a+?)?)?)?)?)?)')
        self.assertTrue(A.isDeterministic())

    def test_determinism_6(self):
        A=OA.fromString('a|(a,(a,(a,(a,(a,(a,a+?)?)?)?)?)?)')
        self.assertFalse(A.isDeterministic())

    def test_eq_1(self):
        A = OA.fromString('a+')
        B = OA.fromString('a*')
        self.assertTrue(equivalentTo(A,A))
        self.assertTrue(equivalentTo(B,B))
        self.assertTrue(equivalentToMEW(A,A))
        self.assertTrue(equivalentToMEW(B,B))
        self.assertTrue(equivalentToMEW(A,B))
        self.assertTrue(equivalentToMEW(B,A))
        self.assertFalse(equivalentTo(B,A))
        self.assertFalse(equivalentTo(A,B))
 
    def test_eq_2(self):
        A = OA.fromString('(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+')
        B = OA.fromString('(a1|b1|c1|d1|a2|b2|c2|d2)+?')
        C = OA.fromString('(a1|b1|c1|d1|a2|b2|c2|d2)+')
        self.assertTrue(equivalentToMEW(A,B))
        self.assertTrue(equivalentToMEW(B,A))
        self.assertTrue(equivalentToMEW(B,C))
        self.assertTrue(equivalentToMEW(C,B))
        self.assertTrue(equivalentToMEW(C,A))
        self.assertTrue(equivalentToMEW(A,C))
        self.assertTrue(equivalentTo(A,A))
        self.assertTrue(equivalentTo(B,B))
        self.assertTrue(equivalentTo(C,C))
        self.assertTrue(equivalentTo(A,B))
        self.assertTrue(equivalentTo(B,A))
        self.assertFalse(equivalentTo(B,C))
        self.assertFalse(equivalentTo(C,B))
        self.assertFalse(equivalentTo(C,A))
        self.assertFalse(equivalentTo(A,C))
    
    def test_eq_3(self):
        A=OA.fromString('(a,(a,(a,(a,(a,(a,a+?)?)?)?)?)?)')
        B=OA.fromString('a+')
        self.assertTrue(equivalentTo(A,B))
        self.assertTrue(equivalentTo(B,A))
        C=OA.fromString('a*')
        self.assertTrue(equivalentToMEW(A,C))
        self.assertTrue(equivalentToMEW(C,A))
        self.assertFalse(equivalentTo(A,C))
        self.assertFalse(equivalentTo(C,A))    
        
    def test_dre_eq_1(self):
        rxA = DRE.fromString('(a*|b)+?')
        rxB = DRE.fromString('(b|a+?)*')
        self.assertEqual(rxA,rxB)
        
    def test_UF(self):
        import modod.uf as uf
        x =uf.UF()
        x.makeset(1)
        x.makeset(2)
        x.makeset(3)
        self.assertEqual(1,x.find(1))
        self.assertEqual(2,x.find(2))
        self.assertEqual(3,x.find(3))
        self.assertNotEqual(1,x.find(2))
        x.union(1,2)
        self.assertEqual(1,x.find(1))
        self.assertEqual(x.find(1),x.find(2))
        self.assertNotEqual(x.find(1),x.find(3))
        self.assertEqual(3,x.find(3))
        
    def test_size_measures_1(self):
        rx = DRE.fromString('(ab,ba,a,b)+')
        self.assertEqual(rx.awidth(),4)
        self.assertEqual(rx.rpn(),8)
        self.assertEqual(rx.size(),10)
        
    def test_size_measures_2(self):
        rx = DRE.fromString('(a,(a,b+))+?')
        self.assertEqual(rx.awidth(),3)
        self.assertEqual(rx.rpn(),8)
        self.assertEqual(rx.size(),12)    
    
    def test_dre_equality_1(self):
        rxA = DRE.fromString('(ab|ba)+')
        rxB = DRE.fromString('(ba|ab)+')
        self.assertEqual(rxA,rxB)
    
    def test_dre_equality_2(self):
        rxA = DRE.fromString('(a?|b+|c?)+')
        rxB = DRE.fromString('(a|b|c)*')
        self.assertNotEqual(rxA,rxB)
        A = OA.fromDRE(rxA)
        B = OA.fromDRE(rxB)
        self.assertTrue(equivalentTo(A,B))

    def test_dre_equality_3(self):
        rxA = DRE.fromString('(a|b|c)+')
        rxB = DRE.fromString('(a|(b|c))+')
        self.assertNotEqual(rxA,rxB)
        self.assertEqual(rxA,rxB.toNNF())

    def test_factorOut_1(self):
        rxA = DRE.fromString('((a,b)|(c,b))?')
        rxB = DRE.fromString('((a|c),b)?')
        self.assertEqual(rxA.factorOut(),rxB)

    def test_factorOut_2(self):
        rxA = DRE.fromString('((a,b+)|b+)')
        rxB = DRE.fromString('(a?,b+)')
        self.assertEqual(rxA.factorOut(),rxB)

    def test_factorOut_3(self):
        rxA = DRE.fromString('((a,b*)|b+)?')
        rxB = DRE.fromString('(a?,b*)')
        self.assertEqual(rxA.factorOut(),rxB)
    
    def test_factorOut_4(self):
        rxA = DRE.fromString('((a,b+)|(c,b*)|b+)')
        rxB = DRE.fromString('((c|(a?,b)),b*)')
        self.assertEqual(rxA.factorOut(),rxB)
    
    def test_factorOut_5(self):
        rxA = DRE.fromString('((a,((b,c?)|c)?)|(b,c?)|c)?')
        rxB = DRE.fromString('(a?,b?,c?)')
        self.assertEqual(rxA.factorOut(),rxB)

    def test_factorOut_6(self):
        rxA = DRE.fromString('(((a1|((a2|(a3,b1)),b2)),b3)|(b1,b2,b3))') # basiert auf Bsp von S. 11/240
        rxB = DRE.fromString('((a1|((a2|(a3?,b1)),b2)),b3)')
        self.assertEqual(rxA.factorOut(),rxB)
    
    def test_factorOut_7(self):
        rxA = DRE.fromString('((a,b+)|(b+)|(c,(a?,b+)?))?') #basiert auf Bsp von S. 12/148f
        rxB = DRE.fromString('(c?,(a?,b+)?)')
        rxC = DRE.fromString('((c,(a?,b+)?)|(b+)|(a,b+))?')
        self.assertEqual(rxA.factorOut(),rxB)
        self.assertEqual(rxC.factorOut(),rxB)

    def test_factorOut_8(self):
        rxA = DRE.fromString('((a,b+)|(c?,b*))')
        rxB = DRE.fromString('(((a,b)|c)?,b*)')
        x = rxA.factorOut()
        open('_tmp.A.dot', 'w').write(rxA.toDOTString())
        open('_tmp.x.dot', 'w').write(x.toDOTString())
        open('_tmp.B.dot', 'w').write(rxB.toDOTString())
        self.assertEqual(rxA.factorOut(),rxB)

if __name__ == '__main__':
    unittest.main()



