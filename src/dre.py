class DRE:
    def graph(self, nodes=None, edges=None):
        if nodes == None:
            nodes, edges = {}, set()
        nodes[len(nodes)] = self.label()
        return nodes, edges

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
        return Terminal(self.symbol)

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

class Optional(Unary):
    def formula(self):
        return '{}?'.format(self.child.formula())
    def label(self):
        return '?'
    pass

class Plus(Unary):
    def formula(self):
        return '{}+'.format(self.child.formula())
    def label(self):
        return '+'
    pass

class Concatenation(Nary):
    def formula(self):
        return '({})'.format(','.join(x.formula() for x in self.children))
    def label(self):
        return ','
    pass

class Choice(Nary):
    def formula(self):
        return '({})'.format('|'.join(x.formula() for x in self.children))
    def label(self):
        return '|'
    pass


