class NonTerm:
    def __init__(self, production):
        self.production = production

class Start(NonTerm):
    pass

class End:
    pass

class grammar:
    # prods: Ein dictionary, das jedem Nichtterminal ein set aller Produktions-
    #        tupel zuweist.
    # start: Ein Nichtterminalsymbol.
    # Die Menge der Nichtterminale besteht aus den Schlüsseln von prods;
    # alle übrigen Symbole, die in Produktionen vorkommen, sind Terminale.
    # Jedes Nichtterminal sollte ein von NonTerm abgeleiteter Typ sein; mindestens
    # muss seine __init__ Funktion eine Liste der produzierten Symbole als einziges
    # Argument akzeptieren.
    def __init__(self, prods, start):
        assert type(prods) is dict, 'Produktionen sind kein dictionary.'
        assert all(type(l) is type and type(r) is set for (l,r) in prods.items()), 'Eine Produktion hat nicht die Form type -> set.'
        assert all(all(type(p) is tuple for p in r) for r in prods.values()), 'Die rechte Seite einer Produktion ist keine Menge von Tupeln.'

        self.prods = prods
        self.start = start
        self.nonterms = set(self.prods.keys())
        self.symbols = {start}
        for production_set in prods.values():
            for production in production_set:
                self.symbols.update(production)

        assert self.nonterms <= self.symbols, 'Unerreichbare Nichtterminale auf der linken Seite.'
        assert type(self.start) is type and start in self.nonterms, 'Startsymbol ist kein Typ, oder nicht produzierbar.'
        assert all(type(s) is type and s not in (Start, End) for s in self.symbols), 'Nicht alle Symbole sind gültige Typen.'

        self.terms = self.symbols - self.nonterms

    def __str__(self):
        return 'Start: {0}\nTerminale: {1}\nNichtterminale: {2}\nProduktionen:\n{3}'.format(
            self.start.__name__,
            ', '.join(x.__name__ for x in self.terms),
            ', '.join(x.__name__ for x in self.nonterms),
            '\n'.join(
                '    {0} → {1}'.format(l.__name__, ' | '.join(
                    (' '.join(x.__name__ for x in p) or 'ε') for p in r
                ))
                for (l, r) in self.prods.items())
        )

    def slr1(self):
        # Beginne mit einer Startproduktion S' -> S $
        start = self.close_state({(Start, (self.start, End), 0)})

        # Berechne rekursiv die Folgezustände.
        nullable = self.nullable()
        first = self.first(nullable)
        follow = self.follow(nullable, first)
        states, shift, reduce = self.derive_states(start, follow, {start})

        return slr1(self.terms, self.nonterms, start, states, shift, reduce)

    # Ein Zustand ist abgeschlossen, wenn für jedes zu lesende
    # Nichtterminal auch jede Produktion enthalten ist.
    def close_state(self, state):
        # Wiederhole, bis keine neuen Produktionen eingefügt werden.
        old, new = 0, len(state)
        while old < new:
            # Welche Nichtterminale können gelesen werden?
            nonterm_shifts = {right[dot] for (left, right, dot) in state if dot < len(right) and right[dot] in self.nonterms}
            # Füge alle deren Produktionen hinzu.
            for left in nonterm_shifts:
                state.update((left, right, 0) for right in self.prods[left])
            old, new = new, len(state)

        # frozenset() ist immutable, und darf daher selbst Element eines sets sein.
        return frozenset(state)

    # Die Zustandsmenge ist abgeschlossen, wenn sie für jeden Zustand und jedes lesbare Zeichen
    # auch den abgeschlossenen Folgezustand enthält.
    def derive_states(self, state, follow, states, shift=None, reduce=None):
        # Initialisiere die shift/reduce Tabellen:
        if shift == reduce == None:
            shift, reduce = {}, {}

        # Berechne die Reduktionsregeln.
        for left, right, dot in state:
            if dot == len(right):
                add_reduce = {(state, lookahead) : (left, right) for lookahead in follow[left]}
                for state, symbol in set(reduce.keys()).intersection(add_reduce.keys()):
                    raise ValueError('Reduce / Reduce-Konflikt.\nZustand: {0}\nLookahead: {1}\nReduktion 1: {2}\nReduktion 2: {3}'.format(
                        state_string(state), symbol.__name__, rule_string(reduce[(state, symbol)]), rule_string(add_reduce[(state, symbol)])
                    ))
                reduce.update(add_reduce)

        # Berechne die Shiftregeln.
        added = set()
        for symbol in {right[dot] for (left, right, dot) in state if dot < len(right)}:
            # Füge den erreichten Zustand hinzu:
            next = self.close_state({(left, right, dot+1) for (left, right, dot) in state if dot < len(right) and right[dot] == symbol})
            if (state, symbol) in reduce:
                raise ValueError('Shift / Reduce-Konflikt.\nZustand: {0}\nLookahead: {1}\nShift: {2}\nReduktion: {3}'.format(
                    state, symbol, next, reduce[(state, symbol)]
                ))
            shift[(state, symbol)] = next
            if next not in states:
                added.add(next)
        states |= added

        # Rekursion für jeden neuen Zustand.
        for state in added:
            self.derive_states(state, follow, states, shift, reduce)

        return states, shift, reduce

    # Bestimme die auf Null produzierenden Nichtterminale
    def nullable(self):
        # Fixpunkt-Iteration
        nullable = {None}
        old, new = 0, 1
        while old < new:
            for left, right in self.prods.items():
                # Falls alle Symbole einer Alternative auf Null produzieren:
                if any(all(t in nullable for t in alt) for alt in right):
                    nullable.add(left)
            old, new = new, len(nullable)
        return nullable.difference([None])

    # Bestimme die ersten Terminale, auf die jedes Nichtterminal produzieren kann.
    def first(self, nullable):
        first = dict([(n,set()) for n in self.nonterms] + [(t,{t}) for t in self.terms] + [(Start, {self.start})])

        # Fixpunkt-Iteration
        old, new = 0, len(self.terms)
        while old < new:
            for left, right in self.prods.items():
                for alt in right:
                    for t in alt:
                        first[left].update(first[t])
                        if t not in nullable:
                            break
            old, new = new, sum(len(x) for x in first.values())
        return first

    # Bestimme alle Lookahead-Symbole für die Reduktion eines Nichtterminals:
    def follow(self, nullable, first):
        direct = {n:set() for n in self.nonterms}
        parents = {n:set() for n in self.nonterms}

        parents[Start] = set()
        direct[Start], direct[self.start] = set(), {End}

        for symbol in self.nonterms:
            # Finde alle Stellen, wo das Symbol rechts in einer Produktion steht:
            for left, right in self.prods.items():
                for alt in right:
                    for i, t in enumerate(alt):
                        if symbol == t:
                            # Bestimme alle ersten Terminalsymbole der Folgekette:
                            for f in alt[i+1:]:
                                direct[symbol] |= first[f]
                                if f not in nullable:
                                    break
                            else:
                                # Wenn die Kette auf das leere Wort produzieren kann, so folge der linken Seite.
                                parents[symbol].add(left)

        # Berechne transitiven Abschluss von parents:
        old, new = 0, sum(len(p) for p in parents.values())
        while old < new:
            for s, p in parents.items():
                parents[s].update(*(parents[x] for x in p))
            old, new = new, sum(len(p) for p in parents.values())

        # Berechne daraus die Follow-Sets:
        follow = {symbol:direct[symbol].union(*(direct[p] for p in parents[symbol])) for symbol in direct}
        return follow

class slr1:
    def __init__(self, terms, nonterms, start, states, shift, reduce):
        self.terms = terms
        self.nonterms = nonterms
        self.start = start
        self.states = states
        self.shift = shift
        self.reduce = reduce
        self.normalize_states()

    # Benenne die Zustände mit Zahlen um.
    def normalize_states(self):
        # Erzeuge eine Numerierung, die mit dem Startzustand beginnt.
        numbering = {self.start : 0}

        for state in self.states.difference({self.start}):
            numbering[state] = len(numbering)
        self.start = 0

        self.shift = {(numbering[state], s): numbering[next] for ((state, s), next) in self.shift.items()}
        self.states = list(range(len(self.states)))
        self.reduce = {(numbering[state], s): rule for ((state, s), rule) in self.reduce.items()}



    # Lese eine Symbolkette
    def parse(self, string, verbose=False):
        # Füge das Endsymbol an.
        string = string + [End()]

        # Zustand-Stack, Symbol-Stack
        states = [self.start]
        symbols = []

        i = 0
        while i < len(string):

            # Versuche shift:
            if (states[-1], type(string[i])) in self.shift:
                states.append(self.shift[(states[-1], type(string[i]))])
                symbols.append(string[i])
                i += 1

            # Versuche zu reduzieren:
            elif (states[-1], type(string[i])) in self.reduce:
                left, right = self.reduce[(states[-1], type(string[i]))]
                # Nehme <length> Symbole vom Stack:
                symbol = left(symbols[len(symbols)-len(right):])
                del symbols[len(symbols)-len(right):], states[len(states)-len(right):]

                symbols.append(symbol)
                states.append(self.shift[(states[-1], left)])
            # Fail:
            else:
                raise ValueError('Unerwartetes token im Zustand %d: %s' % (states[-1], type(string[i]).__name__))
            if verbose:
                print('Stack: [{0}]'.format(', '.join(x.__class__.__name__ for x in symbols)))
                print("State: ", states)
                print('Tokens: [{0}]'.format(', '.join(x.__class__.__name__ for x in string[i:])))
                print('+++')
        return symbols[0]


    def __str__(self):
        namesort = lambda x:x.__name__
        table = []
        symbols = sorted(self.terms, key=namesort) + sorted(self.nonterms, key=namesort)
        table.append(['State', '$'] + [x.__name__ for x in symbols])
        rules = sorted(set(self.reduce.values()), key=lambda x:x[0].__name__)
        lookup = dict(zip(rules, list(range(len(rules)))))
        for state in self.states:
            row = [str(state)]
            if (state, End) in self.reduce:
                row.append('R {0}'.format(lookup[self.reduce[(state, End)]]))
            else:
                row.append('')
            for e in symbols:
                if (state, e) in self.shift:
                    row.append('S {0}'.format(self.shift[(state, e)]))
                elif (state, e) in self.reduce:
                    row.append('R {0}'.format(lookup[self.reduce[(state, e)]]))
                else:
                    row.append('')
            table.append(row)

        rows = []

        return '+++++++++++++\nState Table:\n{0}\n++++++++++\nReductions:\n{1}\n+++++++++++'.format(
            table_string(table),
            '\n'.join('{0}: {1}'.format(i, rule_string(rule)) for (i, rule) in enumerate(rules))
        )

def state_string(state):
    return '{{\n{0}\n}}'.format('\n'.join(
        '  {0} → {1} • {2}'.format(
            l.__name__, ' '.join(x.__name__ for x in r[:dot]), ' '.join(x.__name__ for x in r[dot:])
        )
        for (l, r, dot) in state
    ))

def rule_string(rule):
    return '{0} → {1}'.format(rule[0].__name__, ' '.join(r.__name__ for r in rule[1]))

def table_string(table):
    row_length = max(len(row) for row in table)
    assert all(len(row) == row_length for row in table)
    widths = [max(len(row[j])+2 for row in table) for j in range(row_length)]
    row_width = sum(widths) + row_length + 1
    separator = '\n' + ('+'.join('-'*w for w in widths)) + '\n'
    return separator.join(
        '|'.join(
            cell.center(width) for cell,width in zip(row, widths)
        ) for row in table
    )
