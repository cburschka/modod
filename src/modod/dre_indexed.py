from . import dre

class IndexedDRE:
    def __init__(self, dre):
        self.root = IndexedNodefromDRE(dre)
        self.nodes = list(self.root._dfs())
        self.leaves = [node for node in self.nodes if node.__class__ is Terminal]
        
        for i in range(len(self.nodes) - 1):
            self.nodes[i].l2rdf = self.nodes[i+1]
        for i in range(len(self.nodes)):
            self.nodes[i].node_index = i
        for i, n in enumerate(self.leaves):
            n.leaf_index = i

def IndexedNodefromDRE(dre, parent=None):
    # Determine and defer to sub-type.
    return classes[dre.__class__](dre, parent)

class IndexedNode(dre.DRE):
    def __init__(self, node, parent):
        self.parent = parent
        self.children = []
        for x in node.children:
            self.children.append(IndexedNodefromDRE(x, self))
        for i in range(0, len(node.children)-1):
            self.children[i].right = self.children[i+1]
        for i in range(1, len(node.children)):
            self.children[i].left = self.children[i-1]

    def _dfs(self):
        yield self
        for x in self.children:
            # TODO convert to "yield from" in Python 3.3+
            for y in x._dfs():
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

class Unary(IndexedNode, dre.Unary):
    def __init__(self, node, parent):
        IndexedNode.__init__(self, node, parent)
        self.child = self.children[0]
        
class Plus(Unary, dre.Plus):
    pass
class Optional(Unary, dre.Optional):
    pass
class Concatenation(IndexedNode, dre.Concatenation):
    pass
class Choice(IndexedNode, dre.Choice):
    pass
class Terminal(IndexedNode, dre.Terminal):
    def __init__(self, node, parent):
        IndexedNode.__init__(self, node, parent)
        dre.Terminal.__init__(self, node.symbol)

classes = {
    dre.Plus : Plus,
    dre.Optional : Optional,
    dre.Concatenation : Concatenation,
    dre.Choice : Choice,
    dre.Terminal : Terminal
}
