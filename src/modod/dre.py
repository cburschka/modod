class DRE:
    def graph(self, nodes=None, edges=None):
        if nodes == None:
            nodes, edges = {}, set()
        nodes[len(nodes)] = self.label()
        return nodes, edges

    # Kanonische Form des Ausdrucks
    def formula(self):
        raise NotImplementedError()

    # Beschriftung des Knotens im Baum
    def label(self):
        raise NotImplementedError()

    # Nary-Normal-Form: kein Nary-Operator enthält ein Kind gleichen Typs.
    def nary_normal_form(self):
        raise NotImplementedError()

    # True genau dann wenn der Ausdruck das leere Wort akzeptiert.
    def accepts_empty(self):
        raise NotImplementedError()

    # p•
    def _pnf1(self):
        raise NotImplementedError(self.__class__.__name__ + '::p•')
    # p◦
    def _pnf2(self):
        raise NotImplementedError(self.__class__.__name__ + '::p◦')
    # p▴
    def _pnf3(self):
        raise NotImplementedError(self.__class__.__name__ + '::p▴')
    # p▵
    def _pnf4(self):
        raise NotImplementedError(self.__class__.__name__ + '::p▵')

class Terminal(DRE):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return 'Terminal ["{}"]'.format(self.symbol)

    def formula(self):
        return self.symbol
    def label(self):
        return self.symbol
    def nary_normal_form(self):
        return self
    def accepts_empty(self):
        return False

    def _pnf1(self):
        return self
    def _pnf2(self):
        return self
    def _pnf3(self):
        return self
    def _pnf4(self):
        return self


class Operator(DRE):
    pass

class Unary(Operator):
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return '{} [{}]'.format(self.__class__.__name__, self.child)

    def graph(self, nodes=None, edges=None):
        nodes, edges = DRE.graph(self, nodes, edges)
        edges.add((len(nodes)-1, len(nodes)))
        return self.child.graph(nodes, edges)

    def nary_normal_form(self):
        return self.__class__(self.child.nary_normal_form())

    def _pnf2(self):
        return self.child
    def _pnf3(self):
        return self.__class__(self.child._pnf3())
    def _pnf4(self):
        return self.__class__(self.child._pnf3())

class Nary(Operator):
    def __init__(self, children):
        self.children = children
    def __str__(self):
        return '{} [{}]'.format(self.__class__.__name__, ', '.join(map(str, self.children)))

    def graph(self, nodes=None, edges=None):
        nodes, edges = DRE.graph(self, nodes, edges)
        i = len(nodes) - 1
        for x in self.children:
            edges.add((i, len(nodes)))
            nodes, edges = x.graph(nodes, edges)
        return nodes, edges

    def nary_normal_form(self):
        children = []
        for x in self.children:
            nf = x.nary_normal_form()
            # Direkter Nachfolger gleichen Typs:
            if nf.__class__ == self.__class__:
                children.extend(nf.children)
            else:
                children.append(nf)
        return self.__class__(children)

    def _pnf1(self):
        return self.__class__([x._pnf1() for x in self.children])
    def _pnf4(self):
        return self.__class__([x._pnf3() for x in self.children])

class Optional(Unary):
    def formula(self):
        return '{}?'.format(self.child.formula())
    def label(self):
        return '?'
    def accepts_empty(self):
        return True

    def _pnf1(self):
        x = self.child._pnf1()
        return x if self.child.accepts_empty() else Optional(x)

class Plus(Unary):
    def formula(self):
        return '{}+'.format(self.child.formula())
    def label(self):
        return '+'
    def accepts_empty(self):
        return self.child.is_empty()

    def _pnf1(self):
        x = self.child._pnf1()._pnf2()
        return Optional(Plus(x)) if self.child.accepts_empty() else Plus(x)

class Concatenation(Nary):
    def formula(self):
        return '({})'.format(','.join(x.formula() for x in self.children))
    def label(self):
        return ','
    def accepts_empty(self):
        return all(x.is_empty() for x in self.children)

    def _pnf2(self):
        if self.accepts_empty():
            return Choice([x._pnf2() for x in self.children])
        else:
            return self

    def _pnf3(self):
        return Concatenation([x._pnf3() for x in self.children])

class Choice(Nary):
    def formula(self):
        return '({})'.format('|'.join(x.formula() for x in self.children))
    def label(self):
        return '|'
    def accepts_empty(self):
        return any(x.is_empty() for x in self.children)

    def _pnf2(self):
        return Choice([x._pnf2() for x in self.children])
    def _pnf3(self):
        if self.accepts_empty():
            x = [x._pnf4() for x in self.children]

            # "special"
            if any(x.__class__ is Concatenation and x.accepts_empty() for x in self.children):
                return Choice(x)
            else:
                return Optional(Choice(x))
        else:
            return Choice([self._pnf3() for x in self.children])

