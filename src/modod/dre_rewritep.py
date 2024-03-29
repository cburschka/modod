from modod import dre
from modod import dre_extended as ext

def rewritePlus(rho):
    old, new = None, rho
    while old != new:
        old, new = new, ruleP4(ruleP2(ruleP1(new).toPNF()).toPNF()).toPNF()
    return new

def ruleP1(rho):
    if isinstance(rho, dre.Concatenation):
        c = rho.children
        i = len(c) - 1
        while i > 0:
            # Look for a* expression...
            if isStar(c[i]):
                a = c[i].child.child
                # preceded by a' equivalent to a.
                # (a' must precede a* because of determinism)
                for j in range(i - 1, -1, -1):
                    if conc(c[j:i]).equivalentTo(a):
                        # Replace (...a'a*...) with (...a+...)
                        c = c[:j] + [dre.Plus(a)] + c[i+1:]
                        i = j
                        break
            i -= 1

        return conc([ruleP1(x) for x in c])

    elif isinstance(rho, dre.Nary):
        return rho.__class__([ruleP1(x) for x in rho.children])
    elif isinstance(rho, dre.Unary):
        return rho.__class__(ruleP1(rho.child))
    else:
        return rho

def ruleP2(rho):
    if isinstance(rho, dre.Concatenation):
        c = rho.children
        i = len(c) - 1
        while i > 0:
            # Look for w* expression...
            if isStar(c[i]):
                a = c[i].child.child
                if isinstance(c[i-1], dre.Optional) and isinstance(c[i-1].child, dre.Concatenation):
                    b = c[i-1].child.children
                    for j in range(len(b) - 1, -1, -1):
                        if conc(b[j:]).equivalentTo(a):
                            d = conc([dre.Optional(conc(b[:j])), dre.Plus(a)])
                            c = c[:i-1] + [dre.Optional(d)] + c[i+1:]
                            i -= 1
                            break
            i -= 1
        return conc([ruleP2(x) for x in c])

    elif isinstance(rho, dre.Nary):
        return rho.__class__([ruleP2(x) for x in rho.children])
    elif isinstance(rho, dre.Unary):
        return rho.__class__(ruleP2(rho.child))
    else:
        return rho

def ruleP4(rho, nullable = False):
    if isinstance(rho, dre.Terminal):
        return rho
    elif isinstance(rho, dre.Optional):
        return dre.Optional(ruleP4(rho.child, True))
    elif isinstance(rho, dre.Plus):
        return dre.Plus(ruleP4(rho.child))
    elif isinstance(rho, dre.Choice):
        n = nullable or rho.nullable()
        return choice([ruleP4(x, n) for x in rho.children])
    else:
        if nullable and isStar(rho.children[-1]):
            a = rho.children[-1].child
            b = conc(rho.children[:-1])
            A = a.first()
            bA = pf(A, b)
            if bA.equivalentTo(a.child):
                An = rho.terminals() - A
                bAn = pf(An, b)
                a = dre.Optional(ruleP4(a))
                return dre.Concatenation([dre.Optional(ruleP4(bAn)), a]) if bAn else a
        return conc([ruleP4(x) for x in rho.children])

def conc(children):
    return dre.Concatenation(children) if len(children) > 1 else children[0]

def choice(children):
    return dre.Choice(children) if len(children) > 1 else children[0]

# Returns a DRE with fully eliminated empty symbols.
def pf(a, rho):
    if isinstance(rho, dre.Optional):
        return ext.eliminateEmptySymbol(dre.Optional(pf(a, rho.child)))

    elif isinstance(rho, dre.Concatenation):
        b, c = rho.children[0], conc(rho.children[1:])
        if b.nullable():
            d = pf(a, c)
            # If b is nullable and c projects to the empty set, then
            # remove the leftmost option from b to make it not-nullable.
            if isinstance(d, ext.EmptySet):
                e = conc([pf(a, rlo(b)), c])
            else:
                e = conc([pf(a, b), d])
        else:
            e = conc([pf(a, b), c])

    elif isinstance(rho, dre.Choice):
        e = dre.Choice([pf(a, x) for x in rho.children])

    else:
        # Plus and Terminal:
        return rho if rho.first() <= a else ext.EmptySet()
        
    return ext.eliminateEmptySymbol(e)

def rlo(rho):
    if isinstance(rho, dre.Optional):
        return rho.child
    elif isinstance(rho, dre.Choice):
        return dre.Choice([rlo(x) for x in rho.children])
    elif isinstance(rho, dre.Concatenation):
        return dre.Concatenation([rlo(rho.children[0])] + rho.children[1:])
    else:
        return rho

def isStar(rho):
    return isinstance(rho, dre.Optional) and isinstance(rho.child, dre.Plus)
