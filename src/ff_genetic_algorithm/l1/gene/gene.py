import math
import random


class Gene:

    __slots__ = ('schema', '_value')

    def __init__(self, schema, value=None):
        self.schema = schema
        if value is not None:
            self._value = self._coerce(value)
        else:
            self._value = self._random_init()

    def _coerce(self, value):
        if self.schema.type is float:
            return round(float(value), 3)
        return value

    @property
    def name(self):
        return self.schema.name

    @property
    def value(self):
        return self._value

    def _random_init(self):
        s = self.schema
        if s.choices is not None:
            return random.choice(s.choices)
        if s.type is bool:
            return random.choice([True, False])
        if s.type is int:
            return random.randint(s.range[0], s.range[1])
        if s.type is float:
            return round(s.range[0] + random.random() * (s.range[1] - s.range[0]), 3)

    def _steps(self):
        s = self.schema
        if s.choices is not None:
            return len(s.choices)
        if s.type is bool:
            return 2
        if s.type is int:
            return s.range[1] - s.range[0] + 1
        if s.type is float:
            return int(round((s.range[1] - s.range[0]) * 1000)) + 1

    def bit_length(self):
        return max(1, math.ceil(math.log2(self._steps())))

    def to_bits(self):
        s = self.schema
        n_bits = self.bit_length()

        if s.type is bool:
            return "1" if self._value else "0"

        if s.choices is not None:
            idx = s.choices.index(self._value)
            return format(idx, f"0{n_bits}b")

        if s.type is int:
            idx = self._value - s.range[0]
            return format(idx, f"0{n_bits}b")

        if s.type is float:
            idx = int(round((self._value - s.range[0]) * 1000))
            max_idx = self._steps() - 1
            idx = max(0, min(max_idx, idx))
            return format(idx, f"0{n_bits}b")

    def from_bits(self, bit_str):
        s = self.schema
        idx = int(bit_str, 2)
        max_idx = self._steps() - 1
        idx = min(idx, max_idx)

        if s.type is bool:
            self._value = bool(idx)
        elif s.choices is not None:
            self._value = s.choices[idx]
        elif s.type is int:
            self._value = s.range[0] + idx
        elif s.type is float:
            self._value = round(s.range[0] + idx / 1000, 3)
