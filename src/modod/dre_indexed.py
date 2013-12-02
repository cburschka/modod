from . import dre

class Context:
    def __init__(self, parent, left, right, l2rbf):
        self.parent, self.left, self.right, self.l2rbf = parent, left, right, l2rbf

    def copy(self):
        return Context(self.parent, self.left, self.right, self.l2rbf)

class IndexedDRE:
    def __init__(self, dre):
        self.tree = _indexedFromDRE(dre, Context(None, None, None, None))
        self.nodes = list(tree._bfs())
        self.leaves = [node for node in self.nodes if node.__class__ is Terminal]
        
        for i in range(len(nodes) - 1):
            nodes[i].context.l2rbf = nodes[i+1]
        for i, n in enumerate(self.leaves):
            n.index = i

def _indexedFromDRE(dre, context):
    # Determine and defer to sub-type.
    return classes[self.__class__].__init__(self, dre.children, context)

class IndexedNode(dre.DRE):
    def __init__(self, children, context):
        self.context = context.copy()
        self.children = []
        context.parent = self
        for x in children:
            self.children.append(indexedFromDRE(x, context))
        for i in range(0, len(children)-1):
            self.children[i].context.right = self.children[i].context.l2rbf = self.children[i+1]
        for i in range(1, len(children)):
            self.children[i].context.left = self.children[i-1]

    def _bfs(self):
        for x in self.children:
            yield x
        for x in self.children:
            # TODO convert to "yield from" in Python 3.3+
            for y in x._bfs():
                yield y

    # Baum-Traversierung.
    def getParent(self):
        return self.context.parent
    def leftSibling(self):
        return self.context.left
    def rightSibling(self):
        return self.context.right
    def getNextL2RBF(self):
        return self.context.l2rbf


class Plus(dre.Plus, IndexedNode):
    pass
class Optional(dre.Optional, IndexedNode):
    pass
class Concatenation(dre.Concatenation, IndexedNode):
    pass
class Choice(dre.Choice, IndexedNode):
    pass
class Terminal(dre.Terminal, IndexedNode):
    pass


classes = {
    dre.Plus : Plus,
    dre.Optional : Optional,
    dre.Concatenation : Concatenation,
    dre.Choice : Choice,
    dre.Terminal : Terminal
}
