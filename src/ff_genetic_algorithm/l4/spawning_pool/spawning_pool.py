from ...l2.dna import DNA
from ...l3.dna_pool import DnaPool


class SpawningPool:

    __slots__ = ('_schemas', '_pool')

    def __init__(self, schemas):
        self._schemas = schemas
        self._pool = DnaPool()

    @property
    def size(self):
        return self._pool.size

    def spawn(self):
        while True:
            dna = DNA(self._schemas)
            if self._pool.add(dna):
                return dna

    def spawn_batch(self, n):
        return [self.spawn() for _ in range(n)]

    def contains(self, dna):
        return self._pool.contains(dna)

    def clear(self):
        self._pool = DnaPool()
