class DRE:
    pass
    
class Terminal(DRE):
    def __init__(self, symbol):
        self.symbol = symbol
        
    def __str__(self):
        return self.symbol
    pass
    
class Operator(DRE):
    pass
    
class Unary(Operator):
    def __init__(self, child):
        self.child = child
    pass

class Nary(Operator):
    def __init__(self, children):
        self.children = children
    pass
    
class Optional(Unary):
    def __str__(self):
        return '({0})?'.format(self.child)
    pass
    
class Plus(Unary):
    def __str__(self):
        return '({0})+'.format(self.child)
    pass
    
class Concatenation(Nary):
    def __str__(self):
        return '({0})'.format(','.join(map(str, self.children)))
    pass
    
class Choice(Nary):
    def __str__(self):
        return '({0})'.format('|'.join(map(str, self.children)))
    pass


