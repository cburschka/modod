class UF:
    def __init__(self, iterable):
        self.list = list(iterable)
        self.index = {x:i for i,x in enumerate(self.list)}
        self.parent = list(range(len(self.list)))

    def add(self, x):
        self.index[x] = len(self.list)
        self.parent.append(len(self.list))
        self.list.append(x)

    def union(self, a, b):
        i, j = a.find(a), self.find(b)
        if i != j:
            self.parent[j] = i

    def find(self, x):
        return self.list[self._find(self.index[x])]

    def _find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self._find(self.parent[i])
        return self.parent[i]


