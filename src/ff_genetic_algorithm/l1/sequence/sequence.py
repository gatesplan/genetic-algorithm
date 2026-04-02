from ..gene import Gene


class Sequence:

    __slots__ = ('name', 'children')

    def __init__(self, name, children):
        self.name = name
        self.children = list(children)

    def get(self, name):
        for c in self.children:
            if c.name == name:
                return c
        return None

    def flat(self):
        result = []
        for c in self.children:
            if isinstance(c, Sequence):
                result.extend(c.flat())
            else:
                result.append(c)
        return result
