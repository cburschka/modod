# Christoph Burschka, 2012-2013

# Ein SLR(1)-Parser-Generator.

class Start:
    pass

class End:
    pass

class grammar:
    # prods: Liste der Produktionen. Jede Produktion ist ein Paar-Tupel, dessen
    #        linke Seite ein Typ ist, und dessen rechte Seite ein 
    #        Tupel von Typen ist.
    # start: Ein Nichtterminalsymbol.
    
    # Die Menge der Nichtterminale besteht aus allen Symbolen, die links von einer
    # Produktion stehen; alle übrigen Symbole sind Terminale.
    
    def __init__(self, prods, start):
        assert type(prods) is set, 'Produktionen sind keine Menge.'
        assert all(type(prod) is tuple and len(prod) is 2 for prod in prods), 'Nicht alle Produktionen sind Paare.'
        assert all(type(l) is type and type(r) is tuple for (l,r) in prods), 'Eine Produktion hat nicht die Form (type, tuple).'
        assert all(all(type(t) is type and t not in (Start, End) for t in r) for (l,r) in prods), 'Die rechte Seite einer Produktion besteht nicht aus gültigen Typen.'

        self.prods = prods
        self.start = start

        self.nonterms = {l for (l,r) in prods}
        self.symbols = self.nonterms.union(*(r for (l,r) in prods))
        self.terms = self.symbols - self.nonterms
        
        assert type(start) is type and start in self.nonterms, 'Startsymbol ist kein Typ, oder nicht produzierbar.'
                  
    def __str__(self):
        return 'Start: {0}\nTerminale: {1}\nNichtterminale: {2}\nProduktionen:\n{3}'.format(
            self.start.__name__,
            ', '.join(x.__name__ for x in self.terms),
            ', '.join(x.__name__ for x in self.nonterms),
            '\n'.join(
                '    {0} → {1}'.format(n.__name__, ' | '.join(
                    (' '.join(x.__name__ for x in r) or 'ε') for (l,r) in self.prods if l == n))
                for n in self.nonterms)
        )

    def slr1(self):
        # Beginne mit einer Startproduktion S' -> S $
        start = self.close_state({(Start, (self.start, End), 0)})

        # Berechne rekursiv die Folgezustände.
        nullable = self.nullable()
        first = self.first(nullable)
        follow = self.follow(nullable, first)
        states, shift, reduce = self.derive_states(start, follow, {start})

        return slr1(self.symbols.union([Start, End]), start, states, shift, reduce)

    # Ein Zustand ist abgeschlossen, wenn für jedes zu lesende 
    # Nichtterminal auch jede Produktion enthalten ist.
    def close_state(self, state):
        # Wiederhole, bis keine neuen Produktionen eingefügt werden.
        old, new = 0, len(state)
        while old < new:
            # Welche Nichtterminale können gelesen werden?
            nonterm_shifts = {right[dot] for (left, right, dot) in state if dot < len(right) and right[dot] in self.nonterms}
            # Füge alle deren Produktionen hinzu.
            state.update((left, right, 0) for (left, right) in self.prods if left in nonterm_shifts)
            old, new = new, len(state)
        
        # frozenset() ist immutable, und darf daher selbst Element eines sets sein.
        return frozenset(state)

    # Die Zustandsmenge ist abgeschlossen, wenn sie für jeden Zustand und jedes lesbare Zeichen
    # auch den abgeschlossenen Folgezustand enthält.
    def derive_states(self, state, follow, states, shift={}, reduce={}):
        # Berechne die Reduktionsregeln.
        for left, right, dot in state:
            if dot == len(right):
                add_reduce = {(state, lookahead) : (left, right) for lookahead in follow[left]}
                for key in set(reduce.keys()).intersection(add_reduce.keys()):
                    raise ValueError('Reduce / Reduce-Konflikt.\nZustand: {0}\nLookahead: {1}\nReduktion 1: {2}\nReduktion 2: {3}'.format(
                        state, lookahead, reduce[key], add_reduce[key]
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

    # Bestimme die auf das leere Wort produzierenden Nichtterminale
    def nullable(self):
        # Fixpunkt-Iteration
        nullable = {None}
        old, new = 0, 1
        while old < new:
            for left, right in self.prods:
                if all(t in nullable for t in right):
                    nullable.add(left)
            old, new = new, len(nullable)
        return nullable.difference([None])

    # Bestimme die ersten Terminale, auf die jedes Nichtterminal produzieren kann.
    def first(self, nullable):
        first = dict([(n,set()) for n in self.nonterms] + [(t,{t}) for t in self.terms] + [(Start, {self.start})])

        # Fixpunkt-Iteration
        old, new = 0, len(self.terms)        
        while old < new:
            for left, right in self.prods:
                for r in right:
                    first[left].update(first[r])
                    if r not in nullable:
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
            for left, right in self.prods:
                for i, r in enumerate(right):
                    if symbol == r:
                        # Bestimme alle ersten Terminalsymbole der Folgekette:
                        for f in right[i+1:]:
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
    def __init__(self, symbols, start, states, shift, reduce):
        self.symbols = symbols
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
    def parse(self, string):
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

            print('Stack: [{0}]'.format(', '.join(x.__class__.__name__ for x in symbols)))
            print("State: ", states)
            print('Tokens: [{0}]'.format(', '.join(x.__class__.__name__ for x in string[i:])))
            print('+++')
        return symbols[0]
                
                
    def __str__(self):
        table = []
        symbols = sorted(self.symbols.difference([Start, End]), key=lambda x:x.__name__)
        symbolNames = list(map(lambda x:x.__name__, symbols))
        table.append(['State', '#'] + symbolNames)
        rules = sorted(set(self.reduce.values()), key=lambda x:x[0].__name__)
        lookup = dict(zip(rules, range(len(rules))))
        m = max(map(len, symbolNames))+2
        for state in self.states:
            row = [state]
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
            '\n'.join(["|".join([(str(s) + " "*20)[:m] for s in row]) for row in table]), 
            '\n'.join('{0}: {1} → {2}'.format(i, s.__name__, ' '.join([y.__name__ for y in x])) for (i, (s, x)) in enumerate(rules))
        )

def state_string(state):
    return '{{\n{0}\n}}'.format('\n'.join(
        '  {0} → {1} • {2}'.format(
            l.__name__, ' '.join(x.__name__ for x in r[:dot]), ' '.join(x.__name__ for x in r[dot:])
        )
        for (l, r, dot) in state
    ))
