class digraph:
    def __init__(self, nodes, edges):
        self.v, self.e = nodes, edges
        self.incoming = {}
        self.outgoing = {}
        for x in nodes:
            self.incoming[x] = set()
            self.outgoing[x] = set()
        for a,b in edges:
            self.incoming[b].add(a)
            self.outgoing[a].add(b)

    def xdot(self):
        nodes = ('"{}"[label="{}"];'.format(
            esc(x), (esc(self.v[x]) if type(self.v) is dict else esc(x))
        ) for x in self.v)
        edges = ('"{}" -> "{}"[label="{}"];'.format(
            esc(a), esc(b), (esc(self.e[(a,b)]) if type(self.e) is dict else '')
        ) for (a,b) in self.e)
        return 'digraph {{\n{}\n{}\n}}'.format(
            '\n'.join(nodes),
            '\n'.join(edges)
        )

def esc(string):
    return str(string).replace('\\', '\\\\').replace('"', '\\"')
