class UF:
    def __init__(self, iterable=()):
        self.list = list(iterable)
        self.index = {x:i for i,x in enumerate(self.list)}
        self.parent = list(range(len(self.list)))

    def makeset(self, x):
        self.index[x] = len(self.list)
        self.parent.append(len(self.list))
        self.list.append(x)

    def union(self, a, b):
        i, j = self._find(self.index[a]), self._find(self.index[b])
        if i != j:
            self.parent[j] = i

    def find(self, x):
        return self.list[self._find(self.index[x])]

    def _find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self._find(self.parent[i])
        return self.parent[i]

    def export_sets(self):
        sets = {self._find(i):set() for i in self.parent}
        for i,x in enumerate(self.list):
            sets[self._find(i)].add(x)
        return sets.values()
        
    def __str__(self):
        return ', '.join(map(str, self.export_sets()))

