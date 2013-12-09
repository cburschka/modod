import unittest

from modod.dre import DRE
from modod.oa import OA

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

	def test_pnf_no_side_effects(self):
		rx='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
		pnfrx=DRE.fromString(rx).toNNF().toPNF()
		self.assertEqual(pnfrx.toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)?')
		self.assertEqual(rx,'(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?')

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

	# def test_eq_1(self):
	# 	A = OA.fromString('a+')
	# 	B = OA.fromString('a*')
	# 	self.assertTrue(equivalentTo(A,A))
	# 	self.assertTrue(equivalentTo(B,B))
	# 	self.assertTrue(equivalentToMEW(A,A))
	# 	self.assertTrue(equivalentToMEW(B,B))
	# 	self.assertTrue(equivalentToMEW(A,B))
	# 	self.assertTrue(equivalentToMEW(B,A))
	# 	self.assertFalse(equivalentTo(B,A))
	# 	self.assertFalse(equivalentTo(A,B))
 
	# def test_eq_2(self):
	# 	A = OA.fromString('(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+')
	# 	B = OA.fromString('(a1|b1|c1|d1|a2|b2|c2|d2)+?')
	# 	C = OA.fromString('(a1|b1|c1|d1|a2|b2|c2|d2)+')
	# 	self.assertTrue(equivalentTo(A,A))
	# 	self.assertTrue(equivalentTo(B,B))
	# 	self.assertTrue(equivalentTo(C,C))	
	# 	self.assertTrue(equivalentToMEW(A,B))
	# 	self.assertTrue(equivalentToMEW(B,A))
	# 	self.assertTrue(equivalentToMEW(B,C))
	# 	self.assertTrue(equivalentToMEW(C,B))
	# 	self.assertTrue(equivalentToMEW(C,A))
	# 	self.assertTrue(equivalentToMEW(A,C))
	# 	self.assertTrue(equivalentTo(A,B))
	# 	self.assertTrue(equivalentTo(B,A))
	# 	self.assertFalse(equivalentTo(B,C))
	# 	self.assertFalse(equivalentTo(C,B))
	# 	self.assertFalse(equivalentTo(C,A))
	# 	self.assertFalse(equivalentTo(A,C))
	
	# def test_eq_3(self):
	# 	A=OA.fromString('(a,(a,(a,(a,(a,(a,a+?)?)?)?)?)?)')
	# 	B=OA.fromString('a+')
	# 	self.assertTrue(equivalentTo(A,B))
	# 	self.assertTrue(equivalentTo(B,A))
	# 	C=OA.fromString('a*')
	# 	self.assertTrue(equivalentToMEW(A,C))
	# 	self.assertTrue(equivalentToMEW(C,A))
	# 	self.assertFalse(equivalentTo(A,C))
	# 	self.assertFalse(equivalentTo(C,A))
		
	
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
		
		
if __name__ == '__main__':
	unittest.main()



