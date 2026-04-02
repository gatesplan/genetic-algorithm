from ...l0.gene_schema import GeneSchema
from ...l0.sequence_schema import SequenceSchema
from ...l1.gene import Gene
from ...l1.sequence import Sequence


class DNA:

    __slots__ = ('children',)

    def __init__(self, schemas, values=None):
        parsed = self._parse_values(values) if values else {}
        self.children = []
        for s in schemas:
            if isinstance(s, GeneSchema):
                v = parsed.get(s.name)
                self.children.append(s.create(value=v))
            elif isinstance(s, SequenceSchema):
                sub = {k: v for k, v in parsed.items() if k.startswith(s.name + ".")}
                sub_flat = {k[len(s.name) + 1:]: v for k, v in sub.items()}
                self.children.append(self._create_sequence(s, sub_flat))
            else:
                raise TypeError(f"expected GeneSchema or SequenceSchema, got {type(s)}")

    def _parse_values(self, values):
        if values is None:
            return {}
        return dict(values)

    def _create_sequence(self, schema, flat_values):
        items = []
        for c in schema.children:
            if isinstance(c, GeneSchema):
                v = flat_values.get(c.name)
                items.append(c.create(value=v))
            elif isinstance(c, SequenceSchema):
                sub = {k[len(c.name) + 1:]: v
                       for k, v in flat_values.items()
                       if k.startswith(c.name + ".")}
                items.append(self._create_sequence(c, sub))
        return Sequence(schema.name, items)

    def get(self, name):
        for c in self.children:
            if c.name == name:
                return c
        return None

    def get_path(self, path):
        parts = path.split(".")
        current = self
        for part in parts:
            current = current.get(part)
            if current is None:
                return None
        return current

    def flat(self):
        result = []
        for c in self.children:
            if isinstance(c, Sequence):
                result.extend(c.flat())
            else:
                result.append(c)
        return result

    def to_bits(self):
        return "".join(g.to_bits() for g in self.flat())

    def to_int(self):
        return int(self.to_bits(), 2)

    def from_bits(self, bit_str):
        offset = 0
        for gene in self.flat():
            n = gene.bit_length()
            gene.from_bits(bit_str[offset:offset + n])
            offset += n

    def to_values(self):
        result = {}
        self._collect_values(self.children, "", result)
        return result

    def _collect_values(self, children, prefix, result):
        for c in children:
            key = f"{prefix}{c.name}" if prefix else c.name
            if isinstance(c, Sequence):
                self._collect_values(c.children, key + ".", result)
            else:
                result[key] = c.value
