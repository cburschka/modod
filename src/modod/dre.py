import graph
import modod

class DRE:

    ##############################################################
    # Spezifikation
    ##############################################################

    # Nary-Normal-Form: kein Nary-Operator enthält ein Kind gleichen Typs.
    def toNNF(self):
        return self._nnf()
    def isInNNF(self):
        return self._isnnf()

    # Plus-Normal-Form
    def toPNF(self):
        return self._pnf1()._nnf()._pnf3()._nnf()
    def isInPNF(self):
        pass #TODO

    def label(self):
        return self._label

    # Reduce all empty-set and empty-word symbols in this expression.
    def eliminateEmpty(self):
        return self._eliminateEmpty() if self.containsEmpty() else self
    # Check if this has empty-set or empty-word as a real subexpression.
    def containsEmpty(self):
        return False

    # Set of terminals.
    def terminals(self):
        return set(self.terminalOccurrences().keys())
    # Count how often each terminal occurs.
    def terminalOccurrences(self):
        pass

    # Check if this expression accepts the empty word.
    def nullable(self):
        pass

    # Die erlaubten ersten Zeichen der Worte dieser Sprache:
    def first(self):
        pass

    # size: Anzahl Terminalzeichen, Operatoren, Klammern
    def size(self):
        return self._size(operators=True, parentheses=True)
    # syn/rpn: Anzahl Terminalzeichen, Operatoren
    def rpn(self):
        return self._size(operators=True, parentheses=False)
    # aw/awidth: Anzahl Terminalzeichen
    def awidth(self):
        return self._size(operators=False, parentheses=False)

    # Ausgabe:
    def toString(self):
        pass
    def toDOTString(self):
        nodes, edges = self._graph()
        return graph.digraph(nodes, edges).xdot()
    def toTikZString(self):
        nodes, edges = self._graph()
        return graph.digraph(nodes, edges).tikz() # TODO


    # Semi-Private Methoden (haben keine feste Spezifikation):
    def _pnf1(self):
        '''p•'''
        pass

    def _pnf2(self):
        '''p◦'''
        pass

    def _pnf3(self):
        '''p▴'''
        pass

    def _pnf4(self):
        '''p▵'''
        pass

    def _size(self, operators, parentheses):
        pass

    def nullable(self):
        '''Prüft, ob der Ausdruck "nullbar" ist (d.h. das leere Wort akzeptiert).'''
        pass

    def _graph(self, nodes=None, edges=None):
        if nodes == None:
            nodes, edges = {}, set()
        nodes[len(nodes)] = self.label()
        return nodes, edges

    def __hash__(self):
        return hash((self.__class__, self.__key__()))
    def __eq__(a, b):
        return a.__class__ is b.__class__ and a.__key__() == b.__key__()
    def __key__(a, b):
        return self.__class__
    def __lt__(a, b):
        if a.__class__ != b.__class__:
            return a.__class__.__name__ < b.__class__.__name__
        # The key is always a tuple of orderable types.
        return a.__key__() < b.__key__()

class Terminal(DRE):
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def __key__(self):
        return self.symbol

    def __str__(self):
        return 'Terminal ["{}"]'.format(self.symbol)

    def toString(self):
        return self.symbol
    def label(self):
        return self.symbol
    def _nnf(self):
        return self
    def _isnnf(self):
        return True
    def nullable(self):
        return False

    def _pnf1(self):
        return self
    def _pnf2(self):
        return self
    def _pnf3(self):
        return self
    def _pnf4(self):
        return self

    def _size(self, operators, parentheses):
        return 1

    def terminalOccurrences(self):
        return {self.symbol : 1}

    def first(self):
        return {self.symbol}

class Operator(DRE):
    pass

class Unary(Operator):
    def __init__(self, child):
        self.child = child
        self.children = [child]

    def __key__(self):
        return self.child

    def __str__(self):
        return '{} [{}]'.format(self.__class__.__name__, self.child)

    def _graph(self, nodes=None, edges=None):
        nodes, edges = DRE._graph(self, nodes, edges)
        edges.add((len(nodes)-1, len(nodes)))
        return self.child._graph(nodes, edges)
    def toString(self):
        return self.child.toString() + self.label()
    def _nnf(self):
        return self.__class__(self.child._nnf())
    def _isnnf(self):
        return self.child._isnnf()

    def _pnf2(self):
        return self.child._pnf2()
    def _pnf3(self):
        return self.__class__(self.child._pnf3())

    def _size(self, operators, parentheses):
        return operators + self.child._size(operators, parentheses)
    def terminalOccurrences(self):
        return self.child.terminalOccurrences()

    def first(self):
        return self.child.first()

    def containsEmpty(self):
        return isinstance(self.child, Empty) or self.child.containsEmpty()

class Nary(Operator):
    def __init__(self, children):
        self.children = children

    def __str__(self):
        return self.__class__.__name__ + ' [' + ', '.join(map(str, self.children)) + ']'
    def toString(self):
        return '(' + self.label().join(x.toString() for x in self.children) + ')'
    def _graph(self, nodes=None, edges=None):
        nodes, edges = DRE._graph(self, nodes, edges)
        i = len(nodes) - 1
        for x in self.children:
            edges.add((i, len(nodes)))
            nodes, edges = x._graph(nodes, edges)
        return nodes, edges
    def _nnf(self):
        children = []
        for x in self.children:
            nf = x._nnf()
            # Direkter Nachfolger gleichen Typs:
            if nf.__class__ == self.__class__:
                children.extend(nf.children)
            else:
                children.append(nf)
        return self.__class__(children) if len(children) > 1 else children[0]

    def _isnnf(self):
        return all(self.__class__ != x.__class__ and x._isnnf() for x in self.children)

    def _pnf1(self):
        return self.__class__([x._pnf1() for x in self.children])

    def _size(self, operators, parentheses):
        return 2*parentheses + (len(self.children)-1)*operators + sum(x._size(operators, parentheses) for x in self.children)

    def terminalOccurrences(self):
        count = {}
        for x in self.children:
            for t,c in x.terminalOccurrences().items():
                if t in count:
                    count[t] += c
                else:
                    count[t] = c
        return count

    def containsEmpty(self):
        return any(isinstance(x, Empty) or x.containsEmpty() for x in self.children)

class Optional(Unary):
    _label = '?'

    def nullable(self):
        return True
    def _pnf1(self):
        x = self.child._pnf1()
        return x if self.child.nullable() else Optional(x)
    def _pnf4(self):
        return self.child._pnf3()
    def _eliminateEmpty(self):
        x = self.child.eliminateEmpty()
        return Optional(x) if x else EmptyWord()

    def toString(self):
        if isinstance(self.child, Plus):
            return self.child.child.toString() + '*'
        return Unary.toString(self)

class Plus(Unary):
    _label = '+'

    def nullable(self):
        return self.child.nullable()
    def _pnf1(self):
        x = self.child._pnf1()._pnf2()
        return Optional(Plus(x)) if self.child.nullable() else Plus(x)
    def _pnf4(self):
        return Plus(self.child._pnf3())
    def _eliminateEmpty(self):
        x = self.child.eliminateEmpty()
        return x and Plus(x)

class Concatenation(Nary):
    _label = ','

    def nullable(self):
        return all(x.nullable() for x in self.children)
    def _pnf2(self):
        # Wir unterscheiden drei Fälle:
        # Kein, genau ein oder mehr als ein nicht-nullbares Element
        count, last = 0, 0
        for i,x in enumerate(self.children):
            if not x.nullable():
                count, last = count + 1, i
            if count > 1:
                break

        # Sind alle nullbar, so wird aus der Konkatenation ein Oder
        if count == 0:
            return Choice([x._pnf2() for x in self.children])
        # Steige in das einzigen nicht-nullbare Element ab:
        elif count == 1:
            return Concatenation(self.children[:last] + [self.children[last]._pnf2()] + self.children[last+1:])
        # Sonst ändere nichts
        else:
            return self

    def _pnf3(self):
        return Concatenation([x._pnf3() for x in self.children])
    def _pnf4(self):
        return Concatenation([x._pnf3() for x in self.children])

    def first(self):
        f = set()
        for x in self.children:
            f |= x.first()
            if not x.nullable():
                break
        return f

    def _deterministic(self):
        if not all(x._deterministic() for x in self.children):
            return False
        f = set()
        for x in self.children:
            a, b = x.first(), x._follow()
            if f & x.first():
                return False

            f |= x.first()

    def __key__(self):
        return tuple(self.children)

    def _eliminateEmpty(self):
        a = [x.eliminateEmpty() for x in self.children]
        if any(isinstance(x, EmptySet) for x in a):
            return EmptySet()
        b = [x for x in a if x]
        if len(b) == 0:
            return EmptyWord()
        elif len(b) == 1:
            return b[0]
        else:
            return Concatenation(b)

class Choice(Nary):
    _label = '|'

    def nullable(self):
        return any(x.nullable() for x in self.children)
    def _pnf2(self):
        return Choice([x._pnf2() for x in self.children])
    def _pnf3(self):
        if self.nullable():
            x = [x._pnf4() for x in self.children]
            # Falls eines der Elemente "special" (d.h. eine nullbare Konkatenation) ist
            if any(x.__class__ is Concatenation and x.nullable() for x in self.children):
                return Choice(x)
            else:
                return Optional(Choice(x))
        else:
            return Choice([x._pnf3() for x in self.children])
    def _pnf4(self):
        return self._pnf3()

    def first(self):
        f = set()
        for x in self.children:
            f |= x.first()
        return f

    def _deterministic(self):
        if not all(x._deterministic() for x in self.children):
            return False
        f = [x.first() for x in self.children]
        if any(any(f[i] & f[j] for j in range(i+1,len(f))) for i in range(n)):
            return False
        return True

    def __key__(self):
        children = {x:0 for x in self.children}
        for x in self.children:
            children[x] += 1
        return tuple(sorted(children.items()))

    def _eliminateEmpty(self):
        a = [x.eliminateEmpty() for x in self.children]
        if all(isinstance(x, EmptySet) for x in a):
            return EmptySet()
        b = [x for x in a if x]
        if len(b) == 0:
            return EmptyWord()
        elif len(b) == 1:
            return b[0]
        elif any(isinstance(x, EmptyWord) for x in a):
            return Optional(Choice(b))
        else:
            return Choice(b)

    def toString(self):
        if modod.charGroup >= modod.CHARGROUP_COMPLETE and all(isinstance(x, Terminal) and len(x.symbol) == 1 for x in self.children):
            symbols = sorted({x.symbol for x in self.children})
            start, symbols = symbols[0], symbols[1:]
            runs = [[start]]
            for x in symbols:
                if ord(runs[-1][-1]) + 1 == ord(x):
                    runs[-1].append(x)
                else:
                    runs.append([x])
            runs = [(r[0] + '-' + r[-1]) if len(r) > 2 else ''.join(r) for r in runs]
            return '[{0}]'.format(''.join(runs))
        elif modod.charGroup >= modod.CHARGROUP_PARTIAL and 2 <= sum(isinstance(x, Terminal) and len(x.symbol) == 1 for x in self.children):
            letters = sorted({c for c in self.children if isinstance(c, Terminal) and len(c.symbol) == 1})
            nonterms = [c for c in self.children if not (isinstance(c, Terminal) and len(c.symbol) == 1)]
            return Nary.toString(Choice(nonterms + [Choice(letters)]))
        else:
            return Nary.toString(self)

class Empty(DRE):
    def __bool__(self):
        return False

class EmptySet(Empty):
    def toString(self):
        return '{}'

class EmptyWord(Empty):
    def toString(self):
        return 'ε'
