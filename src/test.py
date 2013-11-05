import dre

print(dre.Plus(dre.Concatenation([dre.Terminal("a"), dre.Choice([dre.Terminal("b"), dre.Plus(dre.Terminal("c"))]), dre.Terminal("a")])))
