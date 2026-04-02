from ...l3.gene_pool import GenePool


class CullingPool:

    __slots__ = ('_pool',)

    def __init__(self):
        self._pool = GenePool()

    @property
    def size(self):
        return self._pool.size

    def mark(self, dna):
        return self._pool.add(dna)

    def seen(self, dna):
        return self._pool.contains(dna)
