import graph

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

    # Menge der Terminalsymbole und deren Anzahl:
    def terminals(self):
        return set(self._count_terms().keys())
    def terminalOccurrences(self):
        return self._count_terms()


    # Die erlaubten ersten Zeichen der Worte dieser Sprache:
    def first(self):
        return self._first()

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
        return self._formula()
    def toDOTString(self):
        nodes, edges = self._graph()
        return graph.digraph(nodes, edges).xdot()
    def toTikZString(self):
        nodes, edges = self._graph()
        return graph.digraph(nodes, edges).tikz() # TODO


    # "Private" Methoden:
    # p•
    def _pnf1(self):
        pass
    # p◦
    def _pnf2(self):
        pass
    # p▴
    def _pnf3(self):
        pass
    # p▵
    def _pnf4(self):
        pass

    def _size(self, operators, parentheses):
        pass

    def _graph(self, nodes=None, edges=None):
        if nodes == None:
            nodes, edges = {}, set()
        nodes[len(nodes)] = self._label()
        print(nodes)
        return nodes, edges

    def __hash__(self):
        return hash((self.__class__, self.__key__()))
    def __eq__(a, b):
        return b.__class__ is b.__class__ and a.__key__() == b.__key__()

class Terminal(DRE):
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def __key__(self):
        return self.symbol

    def __str__(self):
        return 'Terminal ["{}"]'.format(self.symbol)

    def _formula(self):
        return self.symbol
    def _label(self):
        return self.symbol
    def _nnf(self):
        return self
    def _isnnf(self):
        return True
    def _test_empty(self):
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

    def _count_terms(self):
        return {self.symbol : 1}

    def _first(self):
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
    def _formula(self):
        return self.child._formula() + self._label()
    def _nnf(self):
        return self.__class__(self.child._nnf())
    def _isnnf(self):
        return self.child._isnnf()
    def _pnf2(self):
        return self.child._pnf2()
    def _pnf3(self):
        return self.__class__(self.child._pnf3())
    # def _pnf4(self):
    #     return self.__class__(self.child._pnf3())
    def _size(self, operators, parentheses):
        return 1 + self.child._size(operators, parentheses)
    def _count_terms(self):
        return self.child._count_terms()

    def _first(self):
        return self.child._first()

class Nary(Operator):
    def __init__(self, children):
        self.children = children

    def __str__(self):
        return self.__class__.__name__ + ' [' + ', '.join(map(str, self.children)) + ']'
    def _formula(self):
        return '(' + self._label().join(x._formula() for x in self.children) + ')'
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
        return self.__class__(children)

    def _isnnf(self):
        return all(self.__class__ != x.__class__ and x._isnnf() for x in self.children)

    def _pnf1(self):
        return self.__class__([x._pnf1() for x in self.children])
    def _pnf4(self):
        return self.__class__([x._pnf3() for x in self.children])
    def _size(self):
        return 2*parentheses + (n-1)*operators + sum(x._size(operators, parentheses) for x in self.children)

    def _count_terms(self):
        count = {}
        for x in self.children:
            for t,c in x._count_terms().items():
                if t in count:
                    count[t] += c
                else:
                    count[t] = c
        return count

class Optional(Unary):
    def _label(self):
        return '?'
    def _test_empty(self):
        return True
    def _pnf1(self):
        x = self.child._pnf1()
        return x if self.child._test_empty() else Optional(x)
    def _pnf4(self):
        return self.child._pnf3()


class Plus(Unary):
    def _label(self):
        return '+'
    def _test_empty(self):
        return self.child._test_empty()
    def _pnf1(self):
        x = self.child._pnf1()._pnf2()
        return Optional(Plus(x)) if self.child._test_empty() else Plus(x)
    def _pnf4(self):
        return Plus(self.child._pnf3())


class Concatenation(Nary):
    def _label(self):
        return ','
    def _test_empty(self):
        return all(x._test_empty() for x in self.children)
    def _pnf2(self):
        if self._test_empty():
            return Choice([x._pnf2() for x in self.children])
        else:
            return self
    def _pnf3(self):
        return Concatenation([x._pnf3() for x in self.children])

    def _first(self):
        f = set()
        for x in self.children:
            f |= x._first()
            if not x._test_empty():
                break
        return f

    def _deterministic(self):
        if not all(x._deterministic() for x in self.children):
            return False
        f = set()
        for x in self.children:
            a, b = x._first(), x._follow()
            if f & x._first():
                return False
            
            f |= x._first()

    def __key__(self):
        return tuple(self.children)

class Choice(Nary):
    def _label(self):
        return '|'
    def _test_empty(self):
        return any(x._test_empty() for x in self.children)
    def _pnf2(self):
        return Choice([x._pnf2() for x in self.children])
    def _pnf3(self):
        if self._test_empty():
            x = [x._pnf4() for x in self.children]
            # "special"
            if any(x.__class__ is Concatenation and x._test_empty() for x in self.children):
                return Choice(x)
            else:
                return Optional(Choice(x))
        else:
            return Choice([x._pnf3() for x in self.children])

    def _first(self):
        f = set()
        for x in self.children:
            f |= x._first()
        return f

    def _deterministic(self):
        if not all(x._deterministic() for x in self.children):
            return False
        f = [x._first() for x in self.children]
        if any(any(f[i] & f[j] for j in range(i+1,len(f))) for i in range(n)):
            return False
        return True

    def __key__(self):
        children = {x:0 for x in self.children}
        for x in self.children:
            children[x] += 1

