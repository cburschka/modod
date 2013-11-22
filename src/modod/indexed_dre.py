from . import dre

class IndexedTerminal(dre.Terminal):
    def __init__(self, term, n):
        self.symbol = term.symbol
        self.index = n
    def _label(self):
        return '({} {})'.format(self.index, self.symbol)
    def __str__(self):
        return 'Terminal [{}:"{}"]'.format(self.index, self.symbol)

def add_index(node, n=None):
    if n == None:
        return add_index(node, 0)[0]
    if isinstance(node, dre.Terminal):
        return IndexedTerminal(node, n), n+1
    elif isinstance(node, dre.Unary):
        child, m = add_index(node.child, n)
        return node.__class__(child), m
    elif isinstance(node, dre.Nary):
        m = n
        children = []
        for child in node.children:
            child, m = add_index(child, m)
            children.append(child)
        return node.__class__(children), m
