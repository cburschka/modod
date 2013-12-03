from modod import DREfromString
import graph

import unittest
 
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

	# def test_eq_1(self):
	# 	A = DREfromString('a+')
	# 	B = DREfromString('a*')
	# 	self.assertEqual(equivalentTo(A,A),True)
	# 	self.assertEqual(equivalentTo(B,B),True)
	# 	self.assertEqual(equivalentToMEW(A,B),True)
	# 	self.assertEqual(equivalentTo(A,B),False)
 
	# def test_eq_2(self):
	# 	A = DREfromString('a+')
	# 	B = DREfromString('a*')
	# 	self.assertEqual(equivalentTo(A,A),True)
	# 	self.assertEqual(equivalentTo(B,B),True)
	# 	self.assertEqual(equivalentToMEW(A,B),True)
	# 	self.assertEqual(equivalentTo(A,B),False)

	# def test_eq_3(self):
	# 	A = DREfromString('a+')
	# 	B = DREfromString('a*')
	# 	self.assertEqual(equivalentTo(A,A),True)
	# 	self.assertEqual(equivalentTo(B,B),True)
	# 	self.assertEqual(equivalentToMEW(A,B),True)
	# 	self.assertEqual(equivalentTo(A,B),False)
 
if __name__ == '__main__':
	unittest.main()



