import graph
import unittest

from modod import DREfromString
from modod import indexed_dre
#from modod import OccurrenceAutomaton

class TestUM(unittest.TestCase):
 
	def setUp(self):
		pass
 
	def test_pnf_example_4_1(self):
		self.assertEqual(DREfromString('((a? | b?)? |(c? | d?)?)?').toNNF().toPNF().toString(),'(a|b|c|d)?')
		
	def test_pnf_example_4_2(self):
		self.assertEqual(DREfromString('(a? b?)+').toNNF().toPNF().toString(),'(a|b)+?')

	def test_pnf_example_4_3(self):
		self.assertEqual(DREfromString('(a?|(b?,c?))?').toNNF().toPNF().toString(),'(a|(b?,c?))')

	def test_pnf_extra_1(self):
		ist='(a*,b*)+'
		self.assertEqual(DREfromString(ist).toNNF().toPNF().toString(),'(a|b)+?')

	def test_pnf_extra_2(self):
		self.assertEqual(DREfromString('(((a?,b?)+,c*)+,d)').toNNF().toPNF().toString(),'((a|b|c)+?,d)')

	def test_pnf_extra_3(self):
		self.assertEqual(DREfromString('(a*+?+?+?,b*+?+?+?)+').toNNF().toPNF().toString(),'(a|b)+?')

	def test_pnf_extra_4(self):
		ist='(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+'
		self.assertEqual(DREfromString(ist).toNNF().toPNF().toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)+?')

	def test_pnf_extra_5(self):
		ist='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
		self.assertEqual(DREfromString(ist).toNNF().toPNF().toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)?')

	def test_pnf_no_side_effects(self):
		rx='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
		pnfrx=DREfromString(rx).toNNF().toPNF()
		self.assertEqual(pnfrx.toString(),'(a1|b1|c1|d1|a2|b2|c2|d2)?')
		self.assertEqual(rx,'(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?')

	def test_determinism_1(self):
		rxstr = 'a+'
		#self.assertTrue(rxstr.isDeterministic())
		A = OccurrenceAutomaton(import_dre.add_index(DREfromString(rxstr)))
		self.assertTrue(A.isDeterministic())

	def test_determinism_2(self):
		rxstr = '(a)*a'
		#self.assertFalse(rxstr.isDeterministic())
		A = OccurrenceAutomaton(import_dre.add_index(DREfromString(rxstr)))
		self.assertFalse(A.isDeterministic())

	def test_determinism_2(self):
		rxstr = '(ab)|(ac)'
		#self.assertFalse(rxstr.isDeterministic())
		A = OccurrenceAutomaton(import_dre.add_index(DREfromString(rxstr)))
		self.assertFalse(A.isDeterministic())
		
	# def test_eq_1(self):
	# 	rxA = DREfromString('a+')
	# 	rxB = DREfromString('a*')
	# 	A = OccurrenceAutomaton(import_dre.add_index(rxA))
	# 	B = OccurrenceAutomaton(import_dre.add_index(rxB))
	# 	self.assertTrue(equivalentTo(A,A))
	# 	self.assertTrue(equivalentTo(B,B))
	# 	self.assertTrue(equivalentToMEW(A,A))
	# 	self.assertTrue(equivalentToMEW(B,B))
	# 	self.assertTrue(equivalentToMEW(A,B))
	# 	self.assertTrue(equivalentToMEW(B,A))
	# 	self.assertFalse(equivalentTo(B,A))
	# 	self.assertFalse(equivalentTo(A,B))
 
	# def test_eq_2(self):
	# 	rxA = DREfromString('(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+')
	# 	rxB = DREfromString('(a1|b1|c1|d1|a2|b2|c2|d2)+?')
	# 	rxC = DREfromString('(a1|b1|c1|d1|a2|b2|c2|d2)+')
	# 	A = OccurrenceAutomaton(import_dre.add_index(rxA))
	# 	B = OccurrenceAutomaton(import_dre.add_index(rxB))
	# 	C = OccurrenceAutomaton(import_dre.add_index(rxC))	
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
 
if __name__ == '__main__':
	unittest.main()



