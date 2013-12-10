from . import dre_indexed, dre
import itertools
import graph
from . import uf

class OA:
    def __init__(self, first, last, follow, nullable):
        self.first, self.last = first, last
        self.follow, self.nullable = follow, nullable

    # Node and edge sets are not needed during recursive OA generation.
    # Only compute them once the OA is finished.
    def _finalize(self):
        self.nodes = set.union(
            {'Start', 'Accept', 'Error'},
            self.first, self.last,
            {x for (x,y) in self.follow},
            {y for (x,y) in self.follow}
        )

        self.edges = set.union(
            {('Error', 'Error')},
            {('Start', x) for x in self.first},
            {(x, 'Accept') for x in self.last},
            self.follow,
            {('Start', 'Accept')} if self.nullable else set()
        )
        
        self.sigma = {
            x for (x,i) in 
            self.first | self.last | 
            {x for (x,y) in self.follow} | 
            {y for (x,y) in self.follow}
        }

        self._delta = {(q, s) : (s,i) for q, (s,i) in self.follow}
        self._delta.update({('Start', s) : (s,i) for (s,i) in self.first})
        self._delta.update({((s,i), '') : 'Accept' for (s,i) in self.last})

    def delta(self, q, s):
        return self._delta[q,s] if (q,s) in self._delta else 'Error'

    def graph(self):
        return graph.digraph(self.nodes(), self.edges())

    def isDeterministic(self):
        # All states reachable from start must be distinctly labeled.
        if len({x for (x,y) in self.first}) < len(self.first):
            return False

        # Every state's successors must be distinctly labeled.
        adjacency = {x:set() for (x,y) in self.follow}
        for x, (y, i) in self.follow:
            if y in adjacency[x]:
                return False
            adjacency[x].add(y)
        return True

    def fromIndexedDRE(itree):
        a = OA.fromIndexedNode(itree.root)
        a._finalize()
        return a

    def fromIndexedNode(node):
        if isinstance(node, dre_indexed.Terminal):
            first = last = {(node.symbol, node.leaf_index)}
            follow = set()
            nullable = False

        elif isinstance(node, dre.Unary):
            oa = OA.fromIndexedNode(node.child)
            first, last = oa.first, oa.last
            
            if isinstance(node, dre.Optional):
                follow = oa.follow
                nullable = True
            elif isinstance(node, dre.Plus):
                follow = oa.follow | set(itertools.product(last, first))
                nullable = oa.nullable

        elif isinstance(node, dre.Nary):
            oas = list(map(OA.fromIndexedNode, node.children))
            
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

    def equivalentToMEW(A, B):
        VA = {('A', x) for x in A.nodes}
        VB = {('B', x) for x in B.nodes}

        # TODO: Can we reject non-identical alphabets immediately?
        Sigma = A.sigma | B.sigma

        Stack = None
        U = uf.UF(VA | VB)     
        U.union(('A', 'Start'), ('B', 'Start'))
        Stack = (('A', 'Start'), ('B', 'Start')), Stack
        while Stack is not None:
            ((_, qA), (_, qB)), Stack = Stack
            for s in Sigma:
                rA, rB = ('A', A.delta(qA, s)), ('B', B.delta(qB, s))
                if U.find(rA) != U.find(rB):
                    U.union(rA, rB)
                    Stack = (rA, rB), Stack

        Accepting = {('A', x) for x in A.last} | {('B', x) for x in B.last}
        NotAccepting = (VA | VB) - Accepting

        return not any(
            x & Accepting and x & NotAccepting
            for x in U.export_sets()
        )

    def equivalentTo(A, B):
        return A.nullable == B.nullable and A.equivalentToMEW(B)

