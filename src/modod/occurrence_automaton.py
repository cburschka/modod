from . import dre_indexed, dre
import itertools
import graph

def OAfromIndexedDRE(tree):
    return OAfromIndexedNode(tree.root)

def OAfromIndexedNode(node):
    if isinstance(node, dre_indexed.Terminal):
        first = last = {(node.leaf_index, node.symbol)}
        follow = set()
        nullable = False

    elif isinstance(node, dre.Unary):
        oa = OAfromIndexedNode(node.child)
        first, last = oa.first, oa.last
        
        if isinstance(node, dre.Optional):
            follow = oa.follow
            nullable = True
        elif isinstance(node, dre.Plus):
            follow = oa.follow | set(itertools.product(last, first))
            nullable = oa.nullable

    elif isinstance(node, dre.Nary):
        oas = list(map(OAfromIndexedNode, node.children))
        
        # Take the edges of all sub-automata
        follow = set.union(*(x.follow for x in oas))

        if isinstance(node, dre.Choice):
            # Union of all firsts and lasts
            first = set.union(*(x.first for x in oas))
            last = set.union(*(x.last for x in oas))
            nullable = any(x.nullable for x in oas)
            
        elif isinstance(node, dre.Concatenation):
            null = lambda x:x.nullable
            # Union of firsts and lasts as long until a non-nullable is reached
            first = set()
            for x in oas:
                first |= x.first
                if not x.nullable:
                    break
            last = set()
            for x in oas[::-1]:
                last |= x.last
                if not x.nullable:
                    break
            
            # Add edges between sub-automata
            for i in range(len(oas)-1):
                follow |= set(itertools.product(oas[i].last, oas[i+1].first))

            nullable = all(x.nullable for x in oas)

    return OA(first, last, follow, nullable)

class OA:
    def __init__(self, first, last, follow, nullable):
        self.first, self.last = first, last
        self.follow, self.nullable = follow, nullable
        
    def graph(self):
        nodes = {'Start', 'Accept'}
        nodes |= self.first | self.last
        nodes |= {x for (x,y) in self.follow} | {y for (x,y) in self.follow}
        
        edges = {('Start', 'Accept')} if self.nullable else set()
        edges |= {('Start', x) for x in self.first}
        edges |= {(x, 'Accept') for x in self.last}
        edges |= self.follow
        
        return graph.digraph(nodes, edges)

