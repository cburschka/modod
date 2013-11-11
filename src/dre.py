class DRE:
    pass

class Terminal(DRE):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return 'Terminal ["{0}"]'.format(self.symbol)
    def formula(self):
        return self.symbol
    pass

class Operator(DRE):
    pass

class Unary(Operator):
    def __init__(self, child):
        self.child = child
    def __str__(self):
        return '{0} [{1}]'.format(self.__class__.__name__, self.child)
    pass

class Nary(Operator):
    def __init__(self, children):
        self.children = children
    def __str__(self):
        return '{0} [{1}]'.format(self.__class__.__name__, ', '.join(map(str, self.children)))
    pass

class Optional(Unary):
    def formula(self):
        return '({0})?'.format(self.child.formula())
    pass

class Plus(Unary):
    def formula(self):
        return '({0})+'.format(self.child.formula())
    pass

class Concatenation(Nary):
    def formula(self):
        return '({0})'.format(','.join(x.formula() for x in self.children))
    pass

class Choice(Nary):
    def formula(self):
        return '({0})'.format('|'.join(x.formula() for x in self.children))
    pass


