from ..gene_schema import GeneSchema


class SequenceSchema:

    __slots__ = ('name', 'children')

    def __init__(self, name, children):
        if not children:
            raise ValueError("children must not be empty")
        for c in children:
            if not isinstance(c, (GeneSchema, SequenceSchema)):
                raise TypeError(f"child must be GeneSchema or SequenceSchema, got {type(c)}")
        self.name = name
        self.children = list(children)

    def create(self, values=None):
        from ...l1.sequence import Sequence
        items = []
        for c in self.children:
            if isinstance(c, GeneSchema):
                v = values.get(c.name) if values else None
                items.append(c.create(value=v))
            else:
                sub_values = values.get(c.name) if values and isinstance(values.get(c.name), dict) else None
                items.append(c.create(values=sub_values))
        return Sequence(self.name, items)
