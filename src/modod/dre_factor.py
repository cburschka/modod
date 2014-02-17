from . import dre
from . import oa

def factorOut(rho, parnull=False):
    if isinstance(rho, dre.Terminal):
        return rho
    elif isinstance(rho, dre.Plus):
        return dre.Plus(factorOut(rho.child, False))
    elif isinstance(rho, dre.Optional):
        if isinstance(rho.child, dre.Choice):
            return factorOut(rho.child, True)
        else:
            return dre.Optional(factorOut(rho.child, False))
    elif isinstance(rho, dre.Concatenation):
        return concatenate(factorOut(removeRMC(rho)), factorOut(rmc(rho)))
    else:
        rn = parnull or rho.nullable()

        # We will "rewrite" rho in this section. As DRE objects are not
        # modifiable themselves, store a list of rho's children here.
        # While the list's elements may be modified, "deletion" happens
        # in a separate set of indices to keep the numbering fixed.
        rhoChildren = list(rho.children)
        undeleted = set(range(len(rhoChildren)))
        # Discard rho; it will not be used again:
        rho = None

        # Mark everything that isn't a concatenation:
        unmarked = {i for i,x in enumerate(rhoChildren) if isinstance(x, dre.Concatenation)}

        # Pick and mark concatenations:
        while unmarked:
            gamma = unmarked.pop()
            pgamma = rmc(rhoChildren[gamma])
            deletees, reducees = set(), set()

            # Attempt to factor out a + or +? loop.
            if isinstance(pgamma, dre.Plus) or (isinstance(pgamma, dre.Optional) and isinstance(pgamma.child, dre.Plus)):
                # Find matching alternatives, and alternatives with a matching suffix.
                for beta in undeleted - {gamma}:
                    if equivalenceMEW(rhoChildren[beta], pgamma):
                        deletees.add(beta)
                    elif (isinstance(rhoChildren[beta], dre.Concatenation) and equivalenceMEW(rmc(rhoChildren[beta]), pgamma)):
                        reducees.add(beta)

                if reducees or deletees:
                    ns = sum(rmc(rhoChildren[x]).nullable() for x in reducees | {gamma})
                    np = len(reducees | {gamma}) - ns
                    # If the factored-out loop is nullable in some alternatives, but not others.
                    if ns and (np or deletees and not rn):
                        factRwPlus(rhoChildren, undeleted, gamma, reducees, deletees, rn)
                    else:
                        factRw(rhoChildren, undeleted, gamma, reducees, deletees)

            # Factor out other expressions.
            else:
                # Find children whose firsts are in the firsts of gamma's rmc:
                F = {i for i in undeleted - {gamma}
                    if rhoChildren[i].first() <= pgamma.first()}
                if F:
                    orF = choice([rhoChildren[x] for x in F])
                    if pgamma.nullable() and rn:
                        if equivalenceMEW(orF, pgamma):
                            deletees = F
                    elif orF.nullable() and not pgamma.nullable():
                        if equivalenceMEW(orF, pgamma):
                            deletees = F
                    else:
                        if equivalence(orF, pgamma):
                            deletees = F
                for beta in undeleted - {gamma} - deletees:
                    if (isinstance(rhoChildren[beta], dre.Concatenation) and
                        equivalence(rmc(rhoChildren[beta]), pgamma)):
                        reducees.add(beta)

                if deletees or reducees:
                    factRw(rhoChildren, undeleted, gamma, reducees, deletees)
            unmarked &= undeleted

        rho = choice([factorOut(rhoChildren[i]) for i in undeleted])
        if parnull and not rho.nullable():
            rho = dre.Optional(rho)
        return rho

def rmc(a):
    assert isinstance(a, dre.Concatenation)
    return a.children[-1]

def removeRMC(a):
    assert isinstance(a, dre.Concatenation)
    return dre.Concatenation(a.children[:-1]) if len(a.children) > 2 else a.children[0]

def concatenate(a, b):
    a = a.children if isinstance(a, dre.Concatenation) else [a]
    b = b.children if isinstance(b, dre.Concatenation) else [b]
    return dre.Concatenation(a + b)

def choice(z):
    assert z
    children = []
    for x in z:
        if isinstance(x, dre.Choice):
            children.extend(x.children)
        else:
            children.append(x)
    return dre.Choice(children) if len(children) > 1 else children[0]

def factRw(rhoChildren, undeleted, gamma, R, D):
    gammaOne = choice([removeRMC(rhoChildren[beta]) for beta in R | {gamma}])
    if D:
        gammaOne = dre.Optional(gammaOne)
    rhoChildren[gamma] = dre.Concatenation([gammaOne] + [rmc(rhoChildren[gamma])])
    undeleted -= R | D

def factRwPlus(rhoChildren, undeleted, gamma, R, D, rn):
    # Get the loop body - one level below +, or two below +?:
    gammaC = rmc(rhoChildren[gamma])
    if isinstance(gammaC, dre.Optional):
        gammaC = gammaC.child
    gammaC = gammaC.child

    # Split reduced expressions into two groups:
    # Rp: expressions that must be followed by at least one loop iteration
    # Rs: expressions that may be followed by the loop
    Rs, Rp = [], []
    for a in R | {gamma}:
        x = removeRMC(rhoChildren[a])
        if rmc(rhoChildren[a]).nullable():
            Rs.append(x)
        else:
            Rp.append(x)

    # We append gammaC to a choice of Rp prefixes; the expression we will
    # generate will basically have this form:
    # (Rs1|Rs2|...| ((Rp1|Rp2|...),gammaC)) (gammaC+?)
    #               (-------gamma2-------)
    # (--------gamma1---------------------)
    # (Since gammaC is eliminated from at least two expressions, duplicating it
    # once will still be cost-effective.)

    if Rp:
        # If the loop occurs without a prefix, but is not nullable on its own,
        # make the Rp prefixes optional
        if D and not rn:
            gamma2 = concatenate(dre.Optional(choice(Rp)), gammaC)
        else:
            gamma2 = concatenate(choice(Rp), gammaC)
    else:
        gamma2 = gammaC

    gamma1 = choice(Rs + [gamma2])

    if D and rn:
        gamma1 = dre.Optional(gamma1)

    rhoChildren[gamma] = concatenate(gamma1, dre.Optional(dre.Plus((gammaC))))
    undeleted -= R | D

def equivalence(a, b):
    return a.nullable() == b.nullable() and equivalenceMEW(a, b)

def equivalenceMEW(a, b):
    return oa.OA.fromDRE(a).equivalentToMEW(oa.OA.fromDRE(b))
