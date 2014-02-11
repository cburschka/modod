from . import dre

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
    else:
        return rho.__class__(ruleP1(rho.child))

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
                            c = c[:i-1] + dre.Optional(d) + c[i+1:]
                            i -= 1
                            break
            i -= 1
        return conc([ruleP2(x) for x in c])
    
    elif isinstance(rho, dre.Nary):
        return rho.__class__([ruleP2(x) for x in rho.children])
    else:
        return rho.__class__(ruleP2(rho.child))

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
            a = rho.children[-1].child.child
            b = conc(rho.children[:-1])
            A = first(a)
            bA = projfirst(A, b)
            if bA and bA.equivalentTo(a):
                An = term(rho) - A
                bAn = projfirst(An, b)
                a = dre.Optional(ruleP4(a))
                return dre.Concatenation([dre.Optional(ruleP4(bAn)), a]) if bAn else a
        return conc([ruleP4(x) for x in rho.children])

def conc(children):
    return dre.Concatenation(children) if len(children) > 1 else children[0]

def choice(children):
    return dre.Choice(children) if len(children) > 1 else children[0]

# Returns a DRE, None (empty set) or '' (empty word).
def projfirst(a, rho):
    if isinstance(rho, dre.Optional):
        e = projfirst(a, rho.child)
        # None? and ''? are immediately reduced to ''.
        return dre.Optional(e) if e else ''
    elif isinstance(rho, dre.Concatenation):
        c = []
        for i, x in enumerate(rho.children):
            x = projfirst(a, x)
            if x === None:
                # A concatenation containing None is reduced to None.
                return None
            elif x === '':
                # '' is immediately removed from the concatenation.
                continue
            else:
                c.append(x)
            # Keep projecting as long as the prefix remains nullable.
            if not x.nullable():
                c += rho.children[i+1:]
                break
        return conc(c)
    elif isinstance(rho, dre.Choice):
        c = [projfirst(a, x) for x in rho.children]
        # Reduce None and ''.
        d = [x for x if x]
        if d:
            d = choice(d)
            # Add ? if '' was reduced.
            return dre.Optional(d) if '' in c else d
        else:
            # Reduce empty choice to None.
            return None
    else:
        # Plus and Terminal:
        return rho if rho.first() <= a else None

def isStar(rho):
    return isinstance(rho, dre.Optional) and isinstance(rho.child, dre.Plus)
