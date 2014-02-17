from modod import dre

class Empty(dre.DRE):
    def __bool__(self):
        return False

class EmptySet(Empty):
    def toString(self):
        return 'Ø'

class EmptyWord(Empty):
    def toString(self):
        return 'ε'

def reduceChoice(rho):
    if isinstance(rho, dre.Operator):
        x = map(reduceChoice, rho.children)
        if isinstance(rho, dre.Choice):
            x = sorted(set(x))
        return rho.__class__(x)
    else:
        return rho

def reduceNary(rho):
    if isinstance(rho, dre.Operator):
        x = list(map(reduceNary, rho.children))
        if isinstance(rho, dre.Nary) and len(x) == 1:
            return x[0]
        else:
            return rho.__class__(x)
    return rho

def containsEmptySymbol(rho):
    return isinstance(rho, dre.Operator) and any(isinstance(gamma, Empty) or containsEmptySymbol(gamma) for gamma in rho.children)

def eliminateEmptySymbol(rho):
    if containsEmptySymbol(rho):
        return reduceNary(_eliminateEmptySymbol(rho))
    else:
        return rho

def _eliminateEmptySymbol(rho):
    if isinstance(rho, dre.Operator):
        x = list(map(eliminateEmptySymbol, rho.children))
        y = [gamma for gamma in x if not isinstance(gamma, Empty)]
        if isinstance(rho, dre.Choice):
            if any(isinstance(gamma, EmptyWord) for gamma in x):
                return dre.Optional(dre.Choice(y))
            elif y:
                return dre.Choice(y)
            else:
                return EmptySet()
        elif isinstance(rho, dre.Concatenation):
            if any(isinstance(gamma, EmptySet) for gamma in x):
                return EmptySet()
            elif y:
                return dre.Concatenation(y)
            else:
                return EmptyWord()
        elif isinstance(rho, dre.Optional) and not y:
            return EmptyWord()
        elif isinstance(rho, dre.Plus) and not y:
            return x[0]
        else:
            return rho.__class__(y)
    else:
        return self

