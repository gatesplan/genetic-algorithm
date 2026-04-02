import random


class GeneSchema:

    __slots__ = ('name', 'type', 'range', 'choices')

    def __init__(self, name, type=None, *, range=None, choices=None):
        self.name = name
        self.choices = choices

        if choices is not None:
            if len(choices) == 0:
                raise ValueError("choices must not be empty")
            self.type = None
            self.range = None
            return

        if type is None:
            raise ValueError("type or choices is required")

        self.type = type

        if type is bool:
            self.range = None
            return

        if type in (int, float):
            if range is None:
                raise ValueError(f"{type.__name__} requires range")
            if range[0] >= range[1]:
                raise ValueError("range min must be less than max")
            self.range = range
            return

        raise ValueError(f"unsupported type: {type}")

    def create(self, value=None):
        from ...l1.gene import Gene
        return Gene(self, value=value)
