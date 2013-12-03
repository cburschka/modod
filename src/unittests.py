import modod
import graph

import unittest
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
		pass
 
	def test_pnf_example_4_1(self):
		ist='((a? | b?)? |(c? | d?)?)?'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a|b|c|d)?')
		
	def test_pnf_example_4_2(self):
		ist='(a? b?)+'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a|b)+?')

	def test_pnf_example_4_3(self):
		ist='(a?|(b?,c?))?'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a|(b?,c?))')

	def test_pnf_extra_1(self):
		ist='(a*,b*)+'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a|b)+?')

	def test_pnf_extra_2(self):
		ist='(((a?,b?)+,c*)+,d)'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'((a|b|c)+?,d)')

	def test_pnf_extra_3(self):
		ist='(a*+?+?+?,b*+?+?+?)+'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a|b)+?')

	def test_pnf_extra_4(self):
		ist='(((a1?|b1?)?|(c1?|d1?)?)?,((a2?|b2?)?|(c2?|d2?)?)?)+'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a1|b1|c1|d1|a2|b2|c2|d2)+?')

	def test_pnf_extra_5(self):
		ist='(((a1? | b1?)? |(c1? | d1?)?)?|((a2? | b2?)? |(c2? | d2?)?)?)?'
		tree_dre = modod._parserExt.parse(modod._lexerExt.lex(ist), verbose=False).dre().toNNF().toPNF().toString()
		self.assertEqual(tree_dre,'(a1|b1|c1|d1|a2|b2|c2|d2)?')

  
if __name__ == '__main__':
	unittest.main()



