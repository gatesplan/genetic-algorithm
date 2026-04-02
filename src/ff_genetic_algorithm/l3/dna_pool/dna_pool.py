class DnaPool:

    __slots__ = ('_index', '_items')

    def __init__(self):
        self._index = set()
        self._items = []

    @property
    def size(self):
        return len(self._items)

    def add(self, dna):
        key = dna.to_int()
        if key in self._index:
            return False
        self._index.add(key)
        self._items.append(dna)
        return True

    def contains(self, dna):
        return dna.to_int() in self._index

    def remove(self, dna):
        key = dna.to_int()
        if key not in self._index:
            return False
        self._index.discard(key)
        self._items = [d for d in self._items if d.to_int() != key]
        return True

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)
