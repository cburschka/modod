import grammar_strict as gs
import grammar_extended as ge

g1 = gs.build_grammar()
g2 = ge.build_grammar()

print(g1)
print(g1.slr1())
print(g2)
print(g2.slr1())
